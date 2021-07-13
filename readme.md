# Prolog-Python JSON interface
Quick, dirty library I use for calling python from my prolog code  - because I couldn't find anything out of the box.

You extend the `ActionHandler` class in python and return terms (using the crude JSON* classes defined under `pj_protocol.py`). For an example, see `test_protocol.py`. 

You can then call it using the `pljson_client` module. See the source for an example.


### pj_protocol types
NOTE: Variables are not supported. Assumes all terms returned by the server are ground.

* JSONCompound(pred:str, args:list)
    - The equivalent of a prolog list. pred is the predicate name, args is a list of the arguments of the compound. Each arg must be  a primitive or a JSONCompound (or JSONList).
* JSONList(elements: list)  
    - The equivalent of a prolog list.
* JSONActionCompound:
    - Mostly internal: A request from prolog is wrapped in a JSONActionCompound. Use JSONActionCompound.action_compound to retrieve the action.
* JSONResultList:
    - Internal: You really don't have to worry about this.

### Writing an action handler
See `test_protocol.py`

### Using from prolog
Use either `hit_api/3` or `pljson_query/1` (requires `user:pljson_server_url/1` to be declared).

`hit_api(+Url, ?Query, -ResultList)`: Url is the server Url, Query is nonvar and must trigger a valid handler, ResultList is the result return by the handler.

`pljson_query(?Query)`: Calls `hit_api/3` with Url retrieved by calling `user:pljson_server_url(Url)`, and unifies query with each element from ResultList one by one (using `member/2`).

Example here:
First, run 
```bash
$ python3 test_protocol.py 
```

Then from the prolog shell
```prolog
?- assert(pljson_server_url('http://127.0.0.1:8008')).

?- use_module(pljson_client).
true.

?- pljson_client:pljson_query( test_protocol(helloworld, X)).
X = 1626171673 ;
X = time(10, 21, 13).
```
