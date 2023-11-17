"""Tool for the DuckDuckGo search API."""

from typing import Optional, Type
import requests

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools.base import BaseTool


class CustomDDGInput(BaseModel):
    query: str = Field(description="search query to look up")


class CustomDuckDuckGoSearchRun(BaseTool):
    """Tool that queries the DuckDuckGo search API."""

    name: str = "duckduckgo_custom_search"
    description: str = (
        "A wrapper around DuckDuckGo Search. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query."
    )
    args_schema: Type[BaseModel] = CustomDDGInput

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        params = dict(q=query, format='json')
        parsed = requests.get('http://api.duckduckgo.com/', params=params).json()

        results = parsed['RelatedTopics']
        final_result = []

        for r in results:
            if 'Text' in r:
                final_result.append(r['FirstURL'] + ' - ' + r['Text'])

        return "\n- - - - - - - - - - - - - -\n".join(final_result)
