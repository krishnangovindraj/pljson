from time import time

from pljson_server.pj_protocol import JSONCompound
from pljson_server.pj_task_interface import PJTaskInterface
from pljson_server.action_handler import ActionHandler

class TestProtocolTask(ActionHandler):
    """ A simple handler to demonstrate - 
    First argument is echo'd, second argument returns the current timestamp """
    
    # Convention: Define the action_compound's predicate here.
    class TestProtocolPredicate(ActionHandler.ActionPredicate):
        PREDICATE = "test_protocol"
        """ Defines the predicate which this handler handles. In this case, test_protocol/* """
        def __init__(self, echo_what, what_time):
            self.echo_what = echo_what
            self.what_time = what_time
            
        def to_json_compound(self):
            return JSONCompound(TestProtocolTask.TestProtocolPredicate.PREDICATE, [self.echo_what, self.what_time])
    
    def handle(self, action_request):
        """ Must return a list of JSONCompounds answering the query.
        Typically, these would be of the ProtocolPredicate class"""
        requested_predicate = TestProtocolTask.TestProtocolPredicate(*action_request.action_compound.args)
        t = int(time())
        tt = t % 86400
        fancy = JSONCompound('time', [tt//3600, (tt%3600)//60, tt%60])
        return [
            TestProtocolTask.TestProtocolPredicate(requested_predicate.echo_what, t),
            TestProtocolTask.TestProtocolPredicate(requested_predicate.echo_what, fancy),
        ]


# Important to do this.
PJTaskInterface.static_instance.register_task(TestProtocolTask.TestProtocolPredicate.PREDICATE, TestProtocolTask())

# You don't need this part. It't just to have an easy example to run
if __name__ == "__main__":
    from sys import argv
    from pljson_server.json_server import run as jsonserver_run
    if len(argv) == 2:
        jsonserver_run(port=int(argv[1]))
    else:
        jsonserver_run()