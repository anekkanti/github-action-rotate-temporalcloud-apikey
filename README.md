# github-action-rotate-temporalcloud-apikey

Github Action to rotate Temporal Cloud api keys

## Example usage
```yaml
name: Rotate Temporal Cloud API Key
on: [workflow_dispatch]
jobs:
  rotate:
    name: Rotate Temporal Cloud API Key
    runs-on: ubuntu-latest
    steps:
      - name: rotate gcp keys
        uses: anekkanti/github-action-rotate-temporalcloud-apikey@main
        with:
          apikey: "${{ secrets.TEMPORAL_CLOUD_API_KEY }}"
          serviceAccountId: "${{ secrets.TEMPORAL_CLOUD_SERVICE_ACCOUNT_ID }}"
          apikeyNamePrefix: "rotate-temporalcloud-apikey-ci"
          duration: 2
          description: "Apikey used for CI/CD in {{ github.repository }}"
          deleteOldApikeys: true
          personalAccessToken: "${{ secrets.PERSONAL_ACCESS_TOKEN }}"
          repositories: ${{ github.repository }}
          secretName: "TEMPORAL_CLOUD_API_KEY"
```

## Inputs
`apikey` : The Temporal Cloud apikey to use to create new api keys and delete the old ones. Can be the apikey that is being rotated and replaced. Required.

`serviceAccountId` : The Temporal Cloud service account id to use to create new api keys and delete the old ones. Required.

`apikeyNamePrefix` : "The prefix to use for the new apikey name. The new apikey name will be `<apikeyNamePrefix>-<timestamp>`. Required.

`duration` : The number of days for which the new apikey should be valid. Defaults to 30 days.

`description` : The description to use for the new apikey. Optional.

`deleteOldApiKeys` : Whether to delete the old apikeys after creating the new one. The old apikeys will be identified by the prefix `<apikeyNamePrefix>-` and will be deleted. Defaults to `false`.

`personalAccessToken` : Github token that can update secrets in the repos. Required.

`repositories` : List of repositories, separated by comma, to install secrets in. Required.

`secretName` : The name of the github secret to update/create the new apikey in. Required.
