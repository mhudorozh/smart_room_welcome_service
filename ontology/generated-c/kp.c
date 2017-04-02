
#include "ontology.h"


int main()
{
    sslog_ss_init_session();
    register_ontology();
    
    if (ss_join(sslog_get_ss_info(), "KP_1") == -1) {
        printf("Can't join to SS\n");
        return 0;
    }

    printf("\nKP join to SS");

// Set your code.	

    sslog_repo_clean_all();
    sslog_ss_leave_session(sslog_get_ss_info());
    
    printf("\nKP leave SS...\n");

    return 0;
}
