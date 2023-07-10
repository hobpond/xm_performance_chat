from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type
from .xmapi import XMApi

xmapi = XMApi()

class GroupPerformanceInput(BaseModel):
    """Input for getting perfromance for all groups from xMatters"""
    start_time_utc: str = Field(..., description="The start date and time to check for performance in ISO-8601")
    end_time_utc: str = Field(..., description="The start date and time to check for performance in ISO-8601")

class GroupPerformanceTool(BaseTool):
    name = "get_all_group_performance"
    description = "Get the Group performance for all groups from xMatters, when no specific group was mentioned"

    def _run(self, start_time_utc: str, end_time_utc: str):
        return xmapi.get_group_performance(start_time_utc, end_time_utc)

    def _arun(self, start_time_utc: str, end_time_utc: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = GroupPerformanceInput

class OneGroupPerformanceInput(BaseModel):
    """Input for getting Group perfromance from xMatters"""
    target_name: str = Field(..., description="The group uuid or targetName for the group in xMatters")
    start_time_utc: str = Field(..., description="The start date and time to check for performance in ISO-8601")
    end_time_utc: str = Field(..., description="The start date and time to check for performance in ISO-8601")

class OneGroupPerformanceTool(BaseTool):
    name = "get_group_performance"
    description = "Get the Group performance of a given target_name from xMatters"

    def _run(self, target_name: str, start_time_utc: str, end_time_utc: str):
        return xmapi.get_one_group_performance(target_name, start_time_utc, end_time_utc)

    def _arun(self, target_name: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = OneGroupPerformanceInput

class GroupInput(BaseModel):
    """Input for getting details about a Group where the id returned is the group uuid and results include services owned by the group and its supervisors"""
    target_name: str = Field(..., description="The group uuid or targetName for the group in xMatters")

class GroupDetailsTool(BaseTool):
    name = "get_group_details"
    description = "Get the Group details including its supervisors and services owned by group"

    def _run(self, target_name: str):
        return xmapi.get_group(target_name)

    def _arun(self, target_name: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = GroupInput
