# Prompt for processing project briefs
project_prompt_template = """
From the Project Brief below, extract the following Entities & relationships described in the mentioned format 
0. ALWAYS FINISH THE OUTPUT. Never send partial responses
1. First, look for these Entity types in the text and generate as comma-separated format similar to entity type.
   `id` property of each entity must be alphanumeric and must be unique among the entities. You will be referring this property to define the relationship between entities. Do not create new entity types that aren't mentioned below. Document must be summarized and stored inside Project entity under `summary` property. You will have to generate as many entities as needed as per the types below:
    Entity Types:
    label:'Project',id:string,name:string;summary:string //Project mentioned in the brief; `id` property is the full name of the project, in lowercase, with no capital letters, special characters, spaces or hyphens; Contents of original document must be summarized inside 'summary' property
    label:'Technology',id:string,name:string //Technology Entity; `id` property is the name of the technology, in camel-case. Identify as many of the technologies used as possible
    label:'Client',id:string,name:string;industry:string //Client that the project was done for; `id` property is the name of the Client, in camel-case; 'industry' is the industry that the client operates in, as mentioned in the project brief.
    
2. Next generate each relationships as triples of head, relationship and tail. To refer the head and tail entity, use their respective `id` property. Relationship property should be mentioned within brackets as comma-separated. They should follow these relationship types below. You will have to generate as many relationships as needed as defined below:
    Relationship types:
    project|USES_TECH|technology 
    project|HAS_CLIENT|client


3. The output should look like :
{
    "entities": [{"label":"Project","id":string,"name":string,"summary":string}],
    "relationships": ["projectid|USES_TECH|technologyid"]
}

Case Sheet:
{ctext}
"""


# Prompt for processing peoples' profiles
people_prompt_template = """From the list of people below, extract the following Entities & relationships described in the mentioned format 
0. ALWAYS FINISH THE OUTPUT. Never send partial responses
1. First, look for these Entity types in the text and generate as comma-separated format similar to entity type.
   `id` property of each entity must be alphanumeric and must be unique among the entities. You will be referring this property to define the relationship between entities. Do not create new entity types that aren't mentioned below. You will have to generate as many entities as needed as per the types below:
    Entity Types:
    label:'Person',id:string,name:string //Person that the data is about. `id` property is the name of the person, in camel-case. 'name' is the person's name, as spelled in the text.
    label:'Project',id:string,name:string;summary:string //Project mentioned in the profile; `id` property is the full lowercase name of the project, with no capital letters, special characters, spaces or hyphens.
    label:'Technology',id:string,name:string //Technology Entity, as listed in the "skills"-section of every person; `id` property is the name of the technology, in camel-case.
    
3. Next generate each relationships as triples of head, relationship and tail. To refer the head and tail entity, use their respective `id` property. Relationship property should be mentioned within brackets as comma-separated. They should follow these relationship types below. You will have to generate as many relationships as needed as defined below:
    Relationship types:
    person|HAS_SKILLS|technology 
    project|HAS_PEOPLE|person


The output should look like :
{
    "entities": [{"label":"Person","id":string,"name":string}],
    "relationships": ["projectid|HAS_PEOPLE|personid"]
}

Case Sheet:
{ctext}
"""


# Prompt for processing slack messages

slack_prompt_template = """
From the list of messages below, extract the following Entities & relationships described in the mentioned format 
0. ALWAYS FINISH THE OUTPUT. Never send partial responses
1. First, look for these Entity types in the text and generate as comma-separated format similar to entity type.
   `id` property of each entity must be alphanumeric and must be unique among the entities. You will be referring this property to define the relationship between entities. Do not create new entity types that aren't mentioned below. You will have to generate as many entities as needed as per the types below:
    Entity Types:
    label:'Person',id:string,name:string //Person that sent the message. `id` property is the name of the person, in camel-case; for example, "michaelClark", or "emmaMartinez"; 'name' is the person's name, as spelled in the text.
    label:'SlackMessage',id:string,text:string //The Slack-Message that was sent; 'id' property should be the message id, as spelled in the reference. 'text' property is the text content of the message, as spelled in the reference
    
3. Next generate each relationships as triples of head, relationship and tail. To refer the head and tail entity, use their respective `id` property. Relationship property should be mentioned within brackets as comma-separated. They should follow these relationship types below. You will have to generate as many relationships as needed as defined below:
    Relationship types:
    personid|SENT|slackmessageid

The output should look like :
{
    "entities": [{"label":"SlackMessage","id":string,"text":string}],
    "relationships": ["personid|SENT|messageid"]
}

Case Sheet:
{ctext}
"""