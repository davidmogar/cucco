#!/usr/bin/env bash

if [[ "${TRAVIS_PULL_REQUEST}" == "false" ]]; then
    echo 'Submitting report'
    CODECLIMATE_REPO_TOKEN=8eca2b2af30c60b05b6bc5ea848ce2e3d52da97ae0c1f923b612af8461bb2fc3 codeclimate-test-reporter
    codecov
else
    echo 'This is a pull request. Report will not be submitted.'
fi
