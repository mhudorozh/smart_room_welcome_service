#include "ontology.h"



#if INCLUDE_CLASS_USER
class_t *CLASS_USER;
#endif
#if INCLUDE_CLASS_USERPAGE
class_t *CLASS_USERPAGE;
#endif
#if INCLUDE_CLASS_NOTHING
class_t *CLASS_NOTHING;
#endif
#if INCLUDE_CLASS_PAGE
class_t *CLASS_PAGE;
#endif
#if INCLUDE_CLASS_MAPPAGE
class_t *CLASS_MAPPAGE;
#endif
#if INCLUDE_CLASS_THING
class_t *CLASS_THING;
#endif


#if INCLUDE_PROPERTY_HASSURNAME
property_t *PROPERTY_HASSURNAME;
#endif
#if INCLUDE_PROPERTY_HASCONTENT
property_t *PROPERTY_HASCONTENT;
#endif
#if INCLUDE_PROPERTY_HASID
property_t *PROPERTY_HASID;
#endif
#if INCLUDE_PROPERTY_HASNAME
property_t *PROPERTY_HASNAME;
#endif
#if INCLUDE_PROPERTY_HASPATRONYMIC
property_t *PROPERTY_HASPATRONYMIC;
#endif
#if INCLUDE_PROPERTY_HASCITY
property_t *PROPERTY_HASCITY;
#endif



/**
 * @brief Register ontology.
 *
 * It creates all structures, such as classes and properties. Use it firs in your propgramm.
 */
void register_ontology()
{    
    list_t *tmp_node = NULL;    

#if INCLUDE_PROPERTY_HASSURNAME

PROPERTY_HASSURNAME =  (property_t *) malloc(sizeof(property_t));
PROPERTY_HASSURNAME->name = strdup("http://cs.karelia.ru/smartroom_welcome_service#hasSurname");
PROPERTY_HASSURNAME->about = strdup("hasSurname");
//PROPERTY_HASSURNAME->range = ""; //getRange
PROPERTY_HASSURNAME->domain = strdup("http://cs.karelia.ru/smartroom_welcome_service#User"); 
PROPERTY_HASSURNAME->maxcardinality = -1;
PROPERTY_HASSURNAME->mincardinality = -1;
PROPERTY_HASSURNAME->subpropertyof = NULL;
PROPERTY_HASSURNAME->oneof = list_get_new_list();  
PROPERTY_HASSURNAME->rtti = RTTI_PROPERTY;
PROPERTY_HASSURNAME->type = DATATYPEPROPERTY;



sslog_repo_add_entity((void *) PROPERTY_HASSURNAME);

#endif
#if INCLUDE_PROPERTY_HASCONTENT

PROPERTY_HASCONTENT =  (property_t *) malloc(sizeof(property_t));
PROPERTY_HASCONTENT->name = strdup("http://cs.karelia.ru/smartroom_welcome_service#hasContent");
PROPERTY_HASCONTENT->about = strdup("hasContent");
//PROPERTY_HASCONTENT->range = ""; //getRange
PROPERTY_HASCONTENT->domain = strdup("http://cs.karelia.ru/smartroom_welcome_service#Page"); 
PROPERTY_HASCONTENT->maxcardinality = -1;
PROPERTY_HASCONTENT->mincardinality = -1;
PROPERTY_HASCONTENT->subpropertyof = NULL;
PROPERTY_HASCONTENT->oneof = list_get_new_list();  
PROPERTY_HASCONTENT->rtti = RTTI_PROPERTY;
PROPERTY_HASCONTENT->type = DATATYPEPROPERTY;



sslog_repo_add_entity((void *) PROPERTY_HASCONTENT);

#endif
#if INCLUDE_PROPERTY_HASID

PROPERTY_HASID =  (property_t *) malloc(sizeof(property_t));
PROPERTY_HASID->name = strdup("http://cs.karelia.ru/smartroom_welcome_service#hasId");
PROPERTY_HASID->about = strdup("hasId");
//PROPERTY_HASID->range = ""; //getRange
PROPERTY_HASID->domain = strdup("http://cs.karelia.ru/smartroom_welcome_service#UserPage"); 
PROPERTY_HASID->maxcardinality = -1;
PROPERTY_HASID->mincardinality = -1;
PROPERTY_HASID->subpropertyof = NULL;
PROPERTY_HASID->oneof = list_get_new_list();  
PROPERTY_HASID->rtti = RTTI_PROPERTY;
PROPERTY_HASID->type = DATATYPEPROPERTY;



sslog_repo_add_entity((void *) PROPERTY_HASID);

#endif
#if INCLUDE_PROPERTY_HASNAME

PROPERTY_HASNAME =  (property_t *) malloc(sizeof(property_t));
PROPERTY_HASNAME->name = strdup("http://cs.karelia.ru/smartroom_welcome_service#hasName");
PROPERTY_HASNAME->about = strdup("hasName");
//PROPERTY_HASNAME->range = ""; //getRange
PROPERTY_HASNAME->domain = strdup("http://cs.karelia.ru/smartroom_welcome_service#User"); 
PROPERTY_HASNAME->maxcardinality = -1;
PROPERTY_HASNAME->mincardinality = -1;
PROPERTY_HASNAME->subpropertyof = NULL;
PROPERTY_HASNAME->oneof = list_get_new_list();  
PROPERTY_HASNAME->rtti = RTTI_PROPERTY;
PROPERTY_HASNAME->type = DATATYPEPROPERTY;



sslog_repo_add_entity((void *) PROPERTY_HASNAME);

#endif
#if INCLUDE_PROPERTY_HASPATRONYMIC

PROPERTY_HASPATRONYMIC =  (property_t *) malloc(sizeof(property_t));
PROPERTY_HASPATRONYMIC->name = strdup("http://cs.karelia.ru/smartroom_welcome_service#hasPatronymic");
PROPERTY_HASPATRONYMIC->about = strdup("hasPatronymic");
//PROPERTY_HASPATRONYMIC->range = ""; //getRange
PROPERTY_HASPATRONYMIC->domain = strdup("http://cs.karelia.ru/smartroom_welcome_service#User"); 
PROPERTY_HASPATRONYMIC->maxcardinality = -1;
PROPERTY_HASPATRONYMIC->mincardinality = -1;
PROPERTY_HASPATRONYMIC->subpropertyof = NULL;
PROPERTY_HASPATRONYMIC->oneof = list_get_new_list();  
PROPERTY_HASPATRONYMIC->rtti = RTTI_PROPERTY;
PROPERTY_HASPATRONYMIC->type = DATATYPEPROPERTY;



sslog_repo_add_entity((void *) PROPERTY_HASPATRONYMIC);

#endif
#if INCLUDE_PROPERTY_HASCITY

PROPERTY_HASCITY =  (property_t *) malloc(sizeof(property_t));
PROPERTY_HASCITY->name = strdup("http://cs.karelia.ru/smartroom_welcome_service#hasCity");
PROPERTY_HASCITY->about = strdup("hasCity");
//PROPERTY_HASCITY->range = ""; //getRange
PROPERTY_HASCITY->domain = strdup("http://cs.karelia.ru/smartroom_welcome_service#User"); 
PROPERTY_HASCITY->maxcardinality = -1;
PROPERTY_HASCITY->mincardinality = -1;
PROPERTY_HASCITY->subpropertyof = NULL;
PROPERTY_HASCITY->oneof = list_get_new_list();  
PROPERTY_HASCITY->rtti = RTTI_PROPERTY;
PROPERTY_HASCITY->type = DATATYPEPROPERTY;



sslog_repo_add_entity((void *) PROPERTY_HASCITY);

#endif




#if INCLUDE_CLASS_USER

CLASS_USER = (class_t *) malloc(sizeof(class_t));
CLASS_USER->rtti = RTTI_CLASS;
CLASS_USER->classtype =  strdup("http://cs.karelia.ru/smartroom_welcome_service#User");
CLASS_USER->properties = list_get_new_list();  
CLASS_USER->instances = NULL;
CLASS_USER->superclasses = list_get_new_list();  
CLASS_USER->oneof = list_get_new_list();  

sslog_repo_add_entity((void *) CLASS_USER);

#if INCLUDE_PROPERTY_HASPATRONYMIC
tmp_node = list_get_new_node(PROPERTY_HASPATRONYMIC);
list_add_node(tmp_node, CLASS_USER->properties);
#endif
#if INCLUDE_PROPERTY_HASSURNAME
tmp_node = list_get_new_node(PROPERTY_HASSURNAME);
list_add_node(tmp_node, CLASS_USER->properties);
#endif
#if INCLUDE_PROPERTY_HASCITY
tmp_node = list_get_new_node(PROPERTY_HASCITY);
list_add_node(tmp_node, CLASS_USER->properties);
#endif

#endif
#if INCLUDE_CLASS_USERPAGE

CLASS_USERPAGE = (class_t *) malloc(sizeof(class_t));
CLASS_USERPAGE->rtti = RTTI_CLASS;
CLASS_USERPAGE->classtype =  strdup("http://cs.karelia.ru/smartroom_welcome_service#UserPage");
CLASS_USERPAGE->properties = list_get_new_list();  
CLASS_USERPAGE->instances = NULL;
CLASS_USERPAGE->superclasses = list_get_new_list();  
CLASS_USERPAGE->oneof = list_get_new_list();  

sslog_repo_add_entity((void *) CLASS_USERPAGE);

#if INCLUDE_PROPERTY_HASCONTENT
tmp_node = list_get_new_node(PROPERTY_HASCONTENT);
list_add_node(tmp_node, CLASS_USERPAGE->properties);
#endif

#endif
#if INCLUDE_CLASS_NOTHING

CLASS_NOTHING = (class_t *) malloc(sizeof(class_t));
CLASS_NOTHING->rtti = RTTI_CLASS;
CLASS_NOTHING->classtype =  strdup("http://www.w3.org/2002/07/owl#Nothing");
CLASS_NOTHING->properties = list_get_new_list();  
CLASS_NOTHING->instances = NULL;
CLASS_NOTHING->superclasses = list_get_new_list();  
CLASS_NOTHING->oneof = list_get_new_list();  

sslog_repo_add_entity((void *) CLASS_NOTHING);

#if INCLUDE_PROPERTY_HASID
tmp_node = list_get_new_node(PROPERTY_HASID);
list_add_node(tmp_node, CLASS_NOTHING->properties);
#endif
#if INCLUDE_PROPERTY_HASPATRONYMIC
tmp_node = list_get_new_node(PROPERTY_HASPATRONYMIC);
list_add_node(tmp_node, CLASS_NOTHING->properties);
#endif
#if INCLUDE_PROPERTY_HASSURNAME
tmp_node = list_get_new_node(PROPERTY_HASSURNAME);
list_add_node(tmp_node, CLASS_NOTHING->properties);
#endif
#if INCLUDE_PROPERTY_HASNAME
tmp_node = list_get_new_node(PROPERTY_HASNAME);
list_add_node(tmp_node, CLASS_NOTHING->properties);
#endif
#if INCLUDE_PROPERTY_HASCONTENT
tmp_node = list_get_new_node(PROPERTY_HASCONTENT);
list_add_node(tmp_node, CLASS_NOTHING->properties);
#endif
#if INCLUDE_PROPERTY_HASCITY
tmp_node = list_get_new_node(PROPERTY_HASCITY);
list_add_node(tmp_node, CLASS_NOTHING->properties);
#endif

#endif
#if INCLUDE_CLASS_PAGE

CLASS_PAGE = (class_t *) malloc(sizeof(class_t));
CLASS_PAGE->rtti = RTTI_CLASS;
CLASS_PAGE->classtype =  strdup("http://cs.karelia.ru/smartroom_welcome_service#Page");
CLASS_PAGE->properties = list_get_new_list();  
CLASS_PAGE->instances = NULL;
CLASS_PAGE->superclasses = list_get_new_list();  
CLASS_PAGE->oneof = list_get_new_list();  

sslog_repo_add_entity((void *) CLASS_PAGE);

#if INCLUDE_PROPERTY_HASCONTENT
tmp_node = list_get_new_node(PROPERTY_HASCONTENT);
list_add_node(tmp_node, CLASS_PAGE->properties);
#endif

#endif
#if INCLUDE_CLASS_MAPPAGE

CLASS_MAPPAGE = (class_t *) malloc(sizeof(class_t));
CLASS_MAPPAGE->rtti = RTTI_CLASS;
CLASS_MAPPAGE->classtype =  strdup("http://cs.karelia.ru/smartroom_welcome_service#MapPage");
CLASS_MAPPAGE->properties = list_get_new_list();  
CLASS_MAPPAGE->instances = NULL;
CLASS_MAPPAGE->superclasses = list_get_new_list();  
CLASS_MAPPAGE->oneof = list_get_new_list();  

sslog_repo_add_entity((void *) CLASS_MAPPAGE);

#if INCLUDE_PROPERTY_HASCONTENT
tmp_node = list_get_new_node(PROPERTY_HASCONTENT);
list_add_node(tmp_node, CLASS_MAPPAGE->properties);
#endif

#endif
#if INCLUDE_CLASS_THING

CLASS_THING = (class_t *) malloc(sizeof(class_t));
CLASS_THING->rtti = RTTI_CLASS;
CLASS_THING->classtype =  strdup("http://www.w3.org/2002/07/owl#Thing");
CLASS_THING->properties = list_get_new_list();  
CLASS_THING->instances = NULL;
CLASS_THING->superclasses = list_get_new_list();  
CLASS_THING->oneof = list_get_new_list();  

sslog_repo_add_entity((void *) CLASS_THING);


#endif


#if INCLUDE_CLASS_USER
#if INCLUDE_CLASS_THING
tmp_node = list_get_new_node(CLASS_THING);
list_add_node(tmp_node, CLASS_USER->superclasses);
#endif
#endif
#if INCLUDE_CLASS_USERPAGE
#if INCLUDE_CLASS_PAGE
tmp_node = list_get_new_node(CLASS_PAGE);
list_add_node(tmp_node, CLASS_USERPAGE->superclasses);
#endif
#endif
#if INCLUDE_CLASS_NOTHING
#if INCLUDE_CLASS_USER
tmp_node = list_get_new_node(CLASS_USER);
list_add_node(tmp_node, CLASS_NOTHING->superclasses);
#endif
#endif
#if INCLUDE_CLASS_NOTHING
#if INCLUDE_CLASS_USERPAGE
tmp_node = list_get_new_node(CLASS_USERPAGE);
list_add_node(tmp_node, CLASS_NOTHING->superclasses);
#endif
#endif
#if INCLUDE_CLASS_NOTHING
#if INCLUDE_CLASS_MAPPAGE
tmp_node = list_get_new_node(CLASS_MAPPAGE);
list_add_node(tmp_node, CLASS_NOTHING->superclasses);
#endif
#endif
#if INCLUDE_CLASS_PAGE
#if INCLUDE_CLASS_THING
tmp_node = list_get_new_node(CLASS_THING);
list_add_node(tmp_node, CLASS_PAGE->superclasses);
#endif
#endif
#if INCLUDE_CLASS_MAPPAGE
#if INCLUDE_CLASS_PAGE
tmp_node = list_get_new_node(CLASS_PAGE);
list_add_node(tmp_node, CLASS_MAPPAGE->superclasses);
#endif
#endif



}


