pushd backend
uv export --no-hashes --frozen --no-group dev --no-group test --format requirements-txt > requirements.txt
popd