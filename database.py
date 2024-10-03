from pymilvus import MilvusClient
from typing import List, Optional, Union


class FaceMemberDatabase:
    def __init__(self) -> None:
        self.client = MilvusClient(host="localhost", port="19530")
        self.collection_name = "members"
        pass

    def search(
        self,
        data: Union[List[list], list],
        filter: str = "",
        limit: int = 10,
        output_fields: Optional[List[str]] = None,
        search_params: Optional[dict] = None,
        timeout: Optional[float] = None,
        partition_names: Optional[List[str]] = None,
        anns_field: Optional[str] = None,
        **kwargs
    ):
        return self.client.search(
            collection_name=self.collection_name,
            data=data,
            filter=filter,
            limit=limit,
            output_fields=output_fields,
            search_params=search_params,
            timeout=timeout,
            partition_names=partition_names,
            anns_field=anns_field,
            **kwargs
        )
