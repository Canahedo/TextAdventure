Documentation on text retrieval
---------------------------------

text_fetcher(file_name: str, obj_name: str, text_key: str) -> list

Running this command will return the requested text as a list
-file_name will typically be hard coded and will be the name of a json file in assets/text ex: "look"
-obj_name will be the name of the object ex: "porch"
-text_key is a descriptor of which chunk of text to use ex: "default_looktext"


Object template
----------------------------

{
    "name": "template",
    "template_dict": {
            "state_a": "text_1",
            "state_b": "text_2"
            },
}


Text template
-----------------------------

{
    "name" : "template",
    "text_1": ["Even a single line must be in a list"],
    "text_2":[
        "If you need to use multiple",
        "lines, do it like this."
    ]
}


Calling text_fetcher example
--------------------------------

text_fetcher("filename", object.name, object.template_dict["state_a"])

returns ["Even a single line must be in a list"]