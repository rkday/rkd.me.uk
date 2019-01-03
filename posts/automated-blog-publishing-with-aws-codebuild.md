---
title: Automated blog publishing with AWS CodeBuild
published_date: "2019-01-03 12:47:26 +0000"
layout: default.liquid
is_draft: false
---
I was reading <https://carolynvanslyck.com/blog/2017/10/docker-or-gtfo/> recently, and the Side-Project Manifesto ("Don’t do things in such a way that I have to remember how shit works 6 months from now") struck a chord with me. Amongst other things, it's a bit of a pain point when updating this blog - besides writing the posts, I need to remember how to publish and upload it. So as part of revamping my blog (and moving it from Pelican to Cobalt), I decided to set something up so that pushing to Github would automatically publish it.

My blog is hosted on S3, so AWS CodeBuild seemed like a sensible choice - whatever I used would need permission to push to my S3 bucket, and it's more secure to keep that all within AWS than to give a third-party service a key. (Even if the third-party service was something secure and well-known like Travis CI, it still leaves a possibility of a mistake on my part accidentally leaking the key.) Here's a quick overview of what I did to get this working.

As prerequisites, the blog should be hosted on GitHub and you should have a Docker container capable of building it.

- my blog was already source-controlled as <https://github.com/rkday/rkd.me.uk>
- the only Cobalt image on Docker Hub was nine months old (<https://hub.docker.com/r/nott/cobalt/>), so I created <https://hub.docker.com/r/rkday/cobalt/> (from <https://github.com/rkday/cobalt-docker>)

With that out of the way, first, add a `buildspec.yml` file to the repository. Mine looks like this:

```
version: 0.2

phases:
  build:
    commands:
      - cobalt build
artifacts:
  files:
    - '**/*'
  discard-paths: no
base-directory: _site
```

For other static site generators, this will need tweaking - `cobalt build` is what builds the HTML from the source, and `_site` is the folder with the generated HTML.

Now, create an S3 bucket according to <https://docs.aws.amazon.com/AmazonS3/latest/dev/HowDoIWebsiteConfiguration.html>.

Next, in the same region as that S3 bucket, create an AWS CodeBuild build.

- The source should point at the GitHub repository, and be set up to build on new commits to master. (Note that you need to select `Repository in my GitHub account`, not `Public repository`, to get this option.)

![Source screenshot](/static/images/codebuild_source.png)

- The environment should be configured with a `Custom image` pointing at the Docker image that can build the blog. The comand from the `buildspec.yml` file gets run in this container.

![Environment screenshot](/static/images/codebuild_environment.png)

- For the buildspec, just choose `Use a buildspec file`

- In the artifact configuration, set it to publish to the root directory of your S3 bucket, with no packaging and no encryption. (The files that are published are chosen by the `buildspec.yml` file - this just controls where they go.)

![Artifacts screenshot](/static/images/codebuild_artifacts.png)

(I initially tried AWS CodePipeline, but that doesn't quite work for this - it always creates the artifacts in S3 as a zip file - and once I figured out how to get CodeBuild to trigger on new commits, there was no need for CodePipeline.)

With this all set up, my blogging workflow is now nicer - after I push a change to a Markdown file, it shows up on the site after 30 seconds. I can also use standard Git techniques to write drafts (e.g. writing them on a branch) and it's pretty trivial to set up a separate 'staging' branch, which is pushed to a separate S3 bucket and which I can use to make sure changes are good before merging to the master branch and therefore the live site.
