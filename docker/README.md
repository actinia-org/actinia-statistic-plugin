To create a new release, you can use this docker to build the wheel and add
to the release.

The `docker build` command builds the wheel and integrated the build-args for
the github release.

The `docker run` command creates the build and uploads the
before created wheel as asset.


```
git clone git@github.com:mundialis/actinia_statistic_plugin.git
cd actinia_statistic_plugin

tag=0.0
credentials=mygithubuser:mygithubpw

docker build --file docker/Dockerfile --build-arg tag=$tag --build-arg credentials=$credentials --tag actinia_statistic_plugin:build .

docker run --rm actinia_statistic_plugin:build
```
