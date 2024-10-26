import asyncio
import datetime
from temporalio.client import CloudOperationsClient
import temporalio.api.cloud.cloudservice.v1 as cloudservicev1
import temporalio.api.cloud.identity.v1 as identityv1

apiversion = "2024-05-13-00"

async def new_client(api_key: str) -> CloudOperationsClient:
    return await CloudOperationsClient.connect(api_key=api_key, version=apiversion)

async def wait_for_async_operation(client: CloudOperationsClient, async_operation_id: str) -> None:
    while True:
        await asyncio.sleep(1)
        resp = await client.cloud_service.get_async_operation(cloudservicev1.GetAsyncOperationRequest(
            async_operation_id=async_operation_id
        ))
        if resp.async_operation.state == "pending" or resp.async_operation.state == "running":
            continue
        if resp.async_operation.state == "fulfilled":
            break
        raise ValueError("async operation failed with error: " + resp.async_operation.failure_reason)

async def create_apikey(
        client: CloudOperationsClient, 
        service_account_id: str, 
        name: str,
        duration: int,
        description: str
        ) -> (identityv1.ApiKey, str):

    spec: identityv1.ApiKeySpec = identityv1.ApiKeySpec(
        owner_id=service_account_id,
        owner_type="service-account",
        display_name=name,
        expiry_time=datetime.datetime.now() + datetime.timedelta(days=int(duration)),
        description=description,
    )
    create_resp = await client.cloud_service.create_api_key(cloudservicev1.CreateApiKeyRequest(spec=spec))
    await wait_for_async_operation(client, create_resp.async_operation.id)

    get_resp = await client.cloud_service.get_api_key(cloudservicev1.GetApiKeyRequest(key_id=create_resp.key_id))
    return get_resp.api_key, create_resp.token


async def get_all_apikeys(client: CloudOperationsClient, service_account_id: str) -> dict:
    apikeys = []
    pagetoken = ""
    while True:
        results = await client.cloud_service.get_api_keys(cloudservicev1.GetApiKeysRequest(
            owner_id=service_account_id,
            owner_type="service-account",
            page_token=pagetoken,
            page_size=1,
        ))
        apikeys.extend(results.api_keys)
        if results.next_page_token is None or results.next_page_token == '' :
            break
        pagetoken = results.next_page_token
    return apikeys

async def delete_apikey(client: CloudOperationsClient, key_id: str, resource_version: str) -> None:
    delete_resp = await client.cloud_service.delete_api_key(cloudservicev1.DeleteApiKeyRequest(key_id=key_id, resource_version=resource_version))
    await wait_for_async_operation(client, delete_resp.async_operation.id)


