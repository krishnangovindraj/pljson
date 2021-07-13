from typing import Dict

from .pj_protocol import JSONActionRequest, JSONResultList
from .action_handler import ActionHandler

class PJTaskInterface:

    static_instance = None

    def __init__(self):
        self.available_tasks = {}

    def register_task(self, pred_name, handler_class):
        # print("Register task ", pred_name, " to ", handler_class)
        self.available_tasks[pred_name] = handler_class

    def process_request(self, request: Dict):
        action_request = JSONActionRequest.from_dict(request)
        # print(action_request)
        handler = self._resolve_handler(action_request)
        result_list = handler.handle(action_request)
        
        # print([str(r) for r in result_list])
        return JSONResultList( [r.to_json_compound() for r in result_list] )

    def _resolve_handler(self, request: JSONActionRequest) -> ActionHandler:
        handler = None
        from sys import stderr
        if request.action_compound.pred_name in self.available_tasks:
            handler = self.available_tasks[request.action_compound.pred_name]
        else:
            raise NameError("Unknown action: " + request.action_compound.pred_name)
        return handler

PJTaskInterface.static_instance = PJTaskInterface()
