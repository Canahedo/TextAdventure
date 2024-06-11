Documentation on text retrieval
---------------------------------

text_fetcher(file_name: str, name: str, index: str) -> None

Running this command will return the requested text
-file_name will typically be hard coded and will be the name of a file in assets/text
-name will be the name of the object
-index is a descriptor of which chunk of text to use


Object template
----------------------------

{
    "name": "template",
    "template_text": {
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

text_fetcher("text_lookup_doc", object.name, object.template_text["state_a"])

returns "As a songle line.."