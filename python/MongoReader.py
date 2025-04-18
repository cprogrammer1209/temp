"""Mongo client."""

from typing import Dict, Iterable, List, Optional, Union

from llama_index.readers.base import BaseReader
from llama_index.schema import Document


class SimpleMongoReader(BaseReader):
    """Simple mongo reader.

    Concatenates each Mongo doc into Document used by LlamaIndex.

    Args:
        host (str): Mongo host.
        port (int): Mongo port.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        uri: Optional[str] = None,
    ) -> None:
        """Initialize with parameters."""
        try:
            from pymongo import MongoClient
        except ImportError as err:
            raise ImportError(
                "`pymongo` package not found, please run `pip install pymongo`"
            ) from err

        client: MongoClient
        if uri:
            client = MongoClient(uri)
        elif host and port:
            client = MongoClient(host, port)
        else:
            raise ValueError("Either `host` and `port` or `uri` must be provided.")

        self.client = client

    def _flatten(self, texts: List[Union[str, List[str]]]) -> List[str]:
        result = []
        for text in texts:
            result += text if isinstance(text, list) else [text]
        return result

    def lazy_load_data(
        self,
        db_name: str,
        collection_name: str,
        field_names: List[str] = ["text"],
        separator: str = "",
        query_dict: Optional[Dict] = None,
        max_docs: int = 0,
        metadata_names: Optional[List[str]] = None,
    ) -> Iterable[Document]:
        """Load data from the input directory.

        Args:
            db_name (str): name of the database.
            collection_name (str): name of the collection.
            field_names(List[str]): names of the fields to be concatenated.
                Defaults to ["text"]
            separator (str): separator to be used between fields.
                Defaults to ""
            query_dict (Optional[Dict]): query to filter documents. Read more
            at [official docs](https://www.mongodb.com/docs/manual/reference/method/db.collection.find/#std-label-method-find-query)
                Defaults to None
            max_docs (int): maximum number of documents to load.
                Defaults to 0 (no limit)
            metadata_names (Optional[List[str]]): names of the fields to be added
                to the metadata attribute of the Document. Defaults to None

        Returns:
            List[Document]: A list of documents.

        """
        db = self.client[db_name]
        cursor = db[collection_name].find(filter=query_dict or {}, limit=max_docs)
        for item in cursor:
            '''texts = []
            if (len(field_names) != 0):
                for name in field_names:
                    if name in item:
                        texts.append(str(name))
            else:
                for key in item:
                    if(key!='_id'):
                        texts.append(str(item[key]))

            texts = self._flatten(texts)
            text = separator.join(texts)
            
            if metadata_names is None:
                yield Document(text=text)
            else:
                try:
                    if (len(metadata_names)!=0):
                        metadata = {name: item[name] for name in metadata_names}
                    else:
                        metadata = {key: item[key] for key in item if key != '_id'}
                except KeyError as err:
                    raise ValueError(
                        f"{err.args[0]} field not found in Mongo document."
                    ) from err
                yield Document(text=str(metadata))
            '''
            metadata = {key: item[key] for key in item if key != '_id' and isinstance(item[key], str) and item[key]!=''}
            text = ''
            for key in item:
                if key != '_id':
                    if item[key] != '' and isinstance(item[key], str):
                        #text += f'{key}:Empty    '
                    #else:
                        text += f'{key}:{item[key]}    '
            yield Document(text=str(text),metadata=metadata)