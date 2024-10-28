import logging
import os
import asyncio
import datetime
import tmprl
from gh import update_gh_secret


apikey = os.environ["INPUT_APIKEY"]
service_account_id = os.environ["INPUT_SERVICEACCOUNTID"]
apikey_name_prefix = os.environ["INPUT_APIKEYNAMEPREFIX"]
delete_old_apikeys = os.environ["INPUT_DELETEOLDAPIKEYS"]
duration = os.environ["INPUT_DURATION"]
description = os.environ["INPUT_DESCRIPTION"]
gh_token = os.environ["INPUT_PERSONALACCESSTOKEN"]
secret_name = os.environ["INPUT_SECRETNAME"]
owner_repositories = os.environ["INPUT_REPOSITORIES"]

logging.basicConfig(format='%(levelname)s %(message)s', level=logging.INFO)

def generate_apikey_name(prefix: str) -> str:
    return f"{prefix}-{datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}"

async def main():
    client = await tmprl.new_client(api_key=apikey)

    # create new apikey
    ak, token = await tmprl.create_apikey(client, service_account_id, generate_apikey_name(apikey_name_prefix), duration, description)
    logging.info(f"Created a new API Key: {ak.spec.display_name}({ak.id})")

    # update secrets in all repos
    for repo in [x.strip() for x in owner_repositories.split(',')]:
        update_gh_secret(repo, secret_name, token, gh_token)
        logging.info("Updated gh secret {} in {}".format(secret_name, repo))

    # delete old apikeys
    if delete_old_apikeys.casefold() == "true":
        apikeys = await tmprl.get_all_apikeys(client, service_account_id)
        for k in apikeys:
            if k.spec.display_name.startswith(apikey_name_prefix+"-") and k.id != ak.id:
                await tmprl.delete_apikey(client, k.id, k.resource_version)
                logging.info(f"Deleted old API Key: {k.spec.display_name}({k.id})")


if __name__ == "__main__":
    asyncio.run(main())
