
SUBJECTS = [
    "Physics", "Biology", "Chemistry", "Mathematics", "English Language",
    "English Literature", "Computer Science", "History and Civics",
    "Geography", "Physical Education", "Economics"
]

PRONOUNS = {
    "male": {"subj":"He", "obj":"him", "poss":"his", "reflex":"himself"},
    "m": {"subj":"He", "obj":"him", "poss":"his", "reflex":"himself"},
    "boy": {"subj":"He", "obj":"him", "poss":"his", "reflex":"himself"},
    "female": {"subj":"She", "obj":"her", "poss":"her", "reflex":"herself"},
    "f": {"subj":"She", "obj":"her", "poss":"her", "reflex":"herself"},
    "girl": {"subj":"She", "obj":"her", "poss":"her", "reflex":"herself"},
}

BANKS = {
"Physics": {
"Conceptual clarity": [
"Demonstrates excellent conceptual clarity and grasps difficult topics with ease.",
"Has a strong grasp of the subject and good conceptual clarity.",
"Has a sound understanding of basic concepts but needs greater depth.",
"Understands the main concepts but gets confused with finer details.",
"Needs to strengthen conceptual understanding through regular revision and reinforcement.",
],
"Reasoning & application": [
"Applies concepts confidently to unfamiliar and higher-order reasoning problems.",
"Demonstrates strong analytical thinking in reasoning-based questions.",
"Applies concepts accurately and shows sound logical thinking.",
"Applies concepts to familiar situations but needs confidence with unfamiliar problems.",
"Needs more practice applying concepts logically to reasoning questions.",
"Requires guidance to analyse problems and apply concepts effectively.",
],
"Numericals & calculations": [
"Solves numericals confidently using appropriate formulae and accurate working.",
"Approaches numerical problems well and generally arrives at accurate solutions.",
"Understands numerical methods but occasionally makes substitution or calculation errors.",
"Can identify relevant formulae but needs greater accuracy in calculations.",
"Needs regular practice in solving numericals systematically.",
"Requires support in identifying formulae and following solution steps.",
"Needs to be more careful with SI units and conversions.",
"Solves numericals well but needs to avoid careless errors in calculations.",
],
"Graphs": [
"Interprets graphs accurately and draws appropriate conclusions.",
"Understands graphical relationships and uses graphs effectively.",
"Reads graphs correctly but needs confidence with complex relationships.",
"Can extract basic information from graphs but needs better analysis.",
"Needs more practice identifying trends and relationships from graphs.",
"Requires guidance to interpret graphs and connect them with concepts.",
],
"Diagrams & labelling": [
"Draws accurate diagrams and ray diagrams with clear labelling.",
"Demonstrates good diagrammatic skills and presents diagrams neatly.",
"Draws generally correct diagrams but needs greater accuracy and attention to detail.",
"Understands the required diagrams but needs to improve accuracy and clarity.",
"Needs to practise drawing diagrams and ray diagrams more accurately.",
"Needs greater attention to neat and complete labelling.",
],
"Scientific terms & definitions": [
"Uses scientific terminology accurately and gives precise definitions.",
"Recalls laws and definitions accurately and uses appropriate scientific terms.",
"Knows laws and definitions well but needs greater precision in terminology.",
"Understands concepts but needs to recall important laws and definitions accurately.",
"Needs to learn key laws and definitions carefully and reproduce them accurately.",
"Needs to use appropriate scientific and technical terms in explanations.",
"Needs to strengthen recall of laws, definitions and scientific terminology.",
],
"Class participation & work": [
"Participates actively in discussions and responds confidently.",
"Is attentive, engaged and completes work thoroughly and consistently.",
"Participates well and willingly clarifies doubts to deepen understanding.",
"Is attentive in class but could participate more confidently.",
"Usually responds when prompted but needs greater initiative in discussions.",
"Has limited classroom participation and needs to engage more actively.",
"Completes written work but needs greater attention to presentation and detail.",
"Needs greater consistency with written work and attention to completeness.",
],
"Revision & improvement": [
"Regular revision and practice will help consolidate concepts and maintain performance.",
"Needs a structured revision plan to strengthen weaker areas.",
"Needs more regular revision to strengthen previously covered concepts.",
"Should practise more numerical and application-based questions to build confidence.",
"Needs to revise topics in greater detail, focusing on finer points.",
"Regular practice of previous years' questions will strengthen application skills.",
],
},

"Biology": {
"Conceptual understanding": [
"has a very good understanding of biological concepts.",
"has a good grasp of the subject matter and understands processes well.",
"can assimilate difficult biological concepts with ease.",
"Needs to put in efforts to improve his/her concepts",
"His understanding of the concepts is good, and his work displays proper analysis and application of concepts",
],
"Application & reasoning": [
"Applies biological concepts appropriately to answer reasoning questions.",
"Can relate biological processes to the situations given in questions.",
"Needs to strengthen the application of concepts to unfamiliar questions.",
"Uses relevant examples effectively while explaining biological concepts.",
],
"Diagrams & terminology": [
"Diagrams are well drawn and labelled.",
"Needs to label biological diagrams neatly and accurately.",
"Uses appropriate biological terminology in written answers.",
"Needs to use scientific terms more consistently in explanations.",
],
"Data & analysis": [
"Analysis and interpretation of biological data has been done well.",
"Can interpret tables, graphs and experimental observations effectively.",
"Needs to practise analysing data before reaching a conclusion.",
],
"Class participation & work": [
"He comprehends quickly and enthusiastically participates in class discussions.",
"He does neat, thorough work and seeks information independently.",
"He tends to respond only when called out.",
"His class response is very good though volunteering responses more often is desirable.",
],
"Revision & improvement": [
"He needs to follow a structured study and revision plan to bridge the gaps evident in the assessment papers.",
"Regular revision of processes, terminology and diagrams will strengthen his performance.",
"With focus and concerted efforts, he is sure to excel in the subject.",
"A regular study and revision schedule will help him truly excel in the subject.",
],
},

"Chemistry": {
"Conceptual clarity": [
"has a very good understanding of the concepts.",
"has a good grasp over the subject matter.",
"can assimilate difficult subject matter with ease and apply it effectively.",
"Needs to put in efforts to improve his/her concepts",
"His understanding of the concepts is good, and his work displays proper analysis and application of concepts",
],
"Numericals & equations": [
"Uses the correct formulae and applies them appropriately in numerical problems.",
"Can solve numerical problems systematically and reaches the correct answer.",
"Needs to be careful about units and conversions wherever needed.",
"He can recall the correct formula but falters at plugging in the correct values.",
"Needs more practice in balancing chemical equations accurately.",
],
"Chemical language": [
"Uses appropriate chemical terms while explaining concepts.",
"Chemical equations and formulae are generally written correctly.",
"Needs to use correct chemical terminology more consistently.",
"Needs to learn important definitions and laws accurately.",
],
"Diagrams & structures": [
"Chemical structures and diagrams are well drawn and labelled.",
"Needs to improve the neatness and accuracy of chemical structures.",
"Can represent bonding and molecular structures appropriately.",
],
"Application & reasoning": [
"Applies concepts aptly in reasoning questions.",
"Can relate theoretical concepts to chemical reactions and observations.",
"Needs to strengthen the application of concepts to unfamiliar questions.",
],
"Revision & improvement": [
"He needs to follow a structured study and revision plan to bridge the gaps evident in the assessment papers.",
"Solving more numerical and application-based questions would benefit him.",
"Regular revision of reactions, formulae and definitions will strengthen his performance.",
"With focus and concerted efforts, he is sure to excel in the subject.",
],
},

"Mathematics": {
"Conceptual understanding": [
"has a very good understanding of mathematical concepts.",
"has a good grasp of the subject matter and applies concepts appropriately.",
"can assimilate difficult concepts with ease.",
"Needs to put in efforts to improve his/her concepts",
"His understanding of the concepts is good, and his work displays proper analysis and application.",
],
"Problem solving": [
"Approaches problems logically and selects suitable methods.",
"Can apply concepts effectively to solve unfamiliar problems.",
"Demonstrates good reasoning and mathematical thinking.",
"Needs more practice in identifying the appropriate method before beginning a problem.",
"Needs to strengthen problem-solving skills through regular practice.",
],
"Accuracy & presentation": [
"Shows good accuracy in calculations and presents work systematically.",
"His work is neat, clear and logically arranged.",
"Needs to be more careful with signs, calculations and intermediate steps.",
"Needs to read questions thoroughly to avoid avoidable errors.",
],
"Graphs & geometry": [
"Graphs and geometrical constructions are accurate and neatly presented.",
"Can interpret graphs and diagrams effectively.",
"Needs to improve accuracy and neatness in geometrical constructions.",
],
"Class participation & work": [
"He comprehends quickly and enthusiastically participates in class discussions.",
"He does neat, thorough work and seeks information independently.",
"He tends to respond only when called out.",
"His class response is very good though volunteering responses more often is desirable.",
],
"Revision & improvement": [
"He needs to follow a structured study and revision plan to bridge the gaps evident in the assessment papers.",
"Solving previous years' papers is recommended.",
"A regular study and revision schedule will help him truly excel in the subject.",
"With focus and concerted efforts, he is sure to excel in the subject.",
],
},

"English Language": {
"Grammar & accuracy": [
"has a very good understanding of grammatical concepts.",
"uses grammar accurately and appropriately in written work.",
"Needs to strengthen grammatical accuracy and sentence construction.",
"Needs to proofread written work carefully to avoid avoidable errors.",
],
"Vocabulary & expression": [
"uses a varied vocabulary and expresses ideas effectively.",
"has a good command over vocabulary and uses words appropriately.",
"Needs to broaden vocabulary and use more precise words.",
"Can improve expression by choosing vocabulary suited to the context.",
],
"Writing skills": [
"organises ideas logically and writes with clarity and coherence.",
"His written work is well structured and displays good control of language.",
"Needs to develop greater coherence and detail in written responses.",
"Needs to follow the required format and address all aspects of the task.",
],
"Comprehension": [
"understands passages well and supports answers with relevant details.",
"can infer meaning effectively from the given text.",
"Needs to read questions carefully and support answers with textual evidence.",
"Needs more practice in interpreting implied meaning and drawing inferences.",
],
"Class participation": [
"He comprehends quickly and enthusiastically participates in class discussions.",
"He tends to respond only when called out.",
"His class response is very good though volunteering responses more often is desirable.",
],
"Revision & improvement": [
"A regular reading and writing schedule will help him truly excel in the subject.",
"He needs to follow a structured revision plan to strengthen areas of difficulty.",
"Regular editing and proofreading of written work will improve accuracy.",
"With focus and concerted efforts, he is sure to excel in the subject.",
],
},

"English Literature": {
"Understanding of texts": [
"has a very good understanding of the texts studied.",
"shows good grasp of themes, characters and literary ideas.",
"can assimilate difficult literary ideas with ease.",
"Needs to put in efforts to improve his/her understanding of the texts.",
],
"Analysis & interpretation": [
"analyses characters, themes and events with insight.",
"supports interpretations with relevant references to the text.",
"can interpret literary passages thoughtfully and draw sound conclusions.",
"Needs to develop greater depth in analysis rather than relying on narrative.",
],
"Use of evidence": [
"uses appropriate textual references to support written responses.",
"selects relevant details from the text to substantiate ideas.",
"Needs to support literary interpretations with more precise textual evidence.",
],
"Expression & vocabulary": [
"expresses ideas clearly and uses appropriate literary vocabulary.",
"His written work is well structured and displays good control of language.",
"Needs to develop greater precision and sophistication in literary expression.",
],
"Class participation": [
"He comprehends quickly and enthusiastically participates in class discussions.",
"He tends to respond only when called out.",
"His class response is very good though volunteering responses more often is desirable.",
],
"Revision & improvement": [
"He needs to follow a structured study and revision plan to bridge the gaps evident in the assessment papers.",
"Regular revision of themes, characters and key passages will strengthen his performance.",
"With focus and concerted efforts, he is sure to excel in the subject.",
],
},

"Computer Science": {
"Conceptual clarity": [
"has a very good understanding of the concepts.",
"has a good grasp over the subject matter and understands programming concepts well.",
"can assimilate difficult subject matter with ease and apply it effectively.",
"Needs to put in efforts to improve his/her concepts",
],
"Programming & problem solving": [
"can apply programming concepts effectively to solve problems.",
"approaches programming problems logically and systematically.",
"writes programs with a clear understanding of the required logic.",
"Needs more practice in developing algorithms before writing code.",
"Needs to improve debugging skills and identify errors systematically.",
],
"Code quality": [
"writes neat and logically structured programs.",
"uses meaningful variable names and presents code systematically.",
"Needs to improve indentation, organisation and clarity of code.",
],
"Application & reasoning": [
"Applies concepts aptly in reasoning and application-based questions.",
"Can relate theoretical concepts to practical computing situations.",
"Needs to strengthen the application of concepts to unfamiliar problems.",
],
"Class participation & work": [
"He comprehends quickly and enthusiastically participates in class discussions.",
"He does neat, thorough work and seeks information independently.",
"He tends to respond only when called out.",
],
"Revision & improvement": [
"He needs to follow a structured study and revision plan to bridge the gaps evident in the assessment papers.",
"Solving more programming and application-based questions would benefit him.",
"Regular practice of coding questions will strengthen his performance.",
"With focus and concerted efforts, he is sure to excel in the subject.",
],
},

"History and Civics": {
"Conceptual understanding": [
"has a very good understanding of historical and civic concepts.",
"has a good grasp over the subject matter and understands events in context.",
"can assimilate difficult subject matter with ease.",
"Needs to put in efforts to improve his/her understanding of the subject.",
],
"Recall & chronology": [
"recalls important events, dates and developments accurately.",
"can place major events in their correct historical context.",
"Needs to revise important dates, events and constitutional terms regularly.",
],
"Analysis & interpretation": [
"analyses historical events and civic issues with clarity.",
"can identify causes, consequences and links between events.",
"supports answers with relevant facts and examples.",
"Needs to develop greater depth in analysing causes and consequences.",
],
"Answer writing": [
"writes well-structured answers and presents information systematically.",
"uses appropriate historical and civic terminology.",
"Needs to read questions thoroughly and address all parts of the question.",
],
"Class participation": [
"He comprehends quickly and enthusiastically participates in class discussions.",
"He tends to respond only when called out.",
"His class response is very good though volunteering responses more often is desirable.",
],
"Revision & improvement": [
"He needs to follow a structured study and revision plan to bridge the gaps evident in the assessment papers.",
"Regular revision of timelines, key terms and important developments will strengthen his performance.",
"Solving previous years' papers is recommended.",
"With focus and concerted efforts, he is sure to excel in the subject.",
],
},

"Geography": {
"Conceptual understanding": [
"has a very good understanding of geographical concepts.",
"has a good grasp over the subject matter and understands geographical processes well.",
"can assimilate difficult subject matter with ease.",
"Needs to put in efforts to improve his/her concepts.",
],
"Map work & diagrams": [
"maps and diagrams are well drawn, accurate and neatly labelled.",
"interprets maps and geographical diagrams effectively.",
"Needs to improve accuracy and neatness in map work.",
"Needs to label diagrams and maps more carefully.",
],
"Data & interpretation": [
"can interpret tables, graphs and geographical data effectively.",
"Analysis and interpretation of geographical data has been done well.",
"Needs to practise analysing data before reaching a conclusion.",
],
"Application & reasoning": [
"applies geographical concepts aptly to reasoning questions.",
"can relate geographical processes to real-world situations.",
"Needs to strengthen the application of concepts to unfamiliar questions.",
],
"Answer writing": [
"writes well-structured answers and uses appropriate geographical terminology.",
"supports explanations with relevant examples and facts.",
"Needs to read questions thoroughly and include all required details.",
],
"Revision & improvement": [
"He needs to follow a structured study and revision plan to bridge the gaps evident in the assessment papers.",
"Regular revision of maps, terms and geographical processes will strengthen his performance.",
"Solving previous years' papers is recommended.",
"With focus and concerted efforts, he is sure to excel in the subject.",
],
},

"Physical Education": {
"Conceptual understanding": [
"has a very good understanding of the concepts related to physical education.",
"has a good grasp of the subject matter and understands rules and principles well.",
"can assimilate difficult subject matter with ease.",
"Needs to put in efforts to improve his/her understanding of the subject.",
],
"Application of knowledge": [
"applies knowledge of rules, techniques and principles effectively.",
"can relate theoretical concepts to practical sporting situations.",
"Needs to strengthen the application of concepts to unfamiliar situations.",
],
"Practical skills": [
"demonstrates good understanding and execution of the skills taught.",
"performs practical activities with confidence and enthusiasm.",
"Needs to improve technique through regular and focused practice.",
"Needs to work on consistency while performing practical skills.",
],
"Fitness & participation": [
"participates actively and enthusiastically in physical activities.",
"shows good awareness of fitness and the importance of regular activity.",
"Needs to participate more consistently in practical activities.",
],
"Class participation & work": [
"He comprehends quickly and enthusiastically participates in class discussions.",
"He does neat, thorough work and seeks information independently.",
"He tends to respond only when called out.",
],
"Revision & improvement": [
"He needs to follow a structured study and revision plan to bridge the gaps evident in the assessment papers.",
"Regular revision of rules, terminology and training principles will strengthen his performance.",
"With focus and concerted efforts, he is sure to excel in the subject.",
"A regular study and revision schedule will help him truly excel in the subject.",
],
},

"Economics": {
"Conceptual understanding": [
"has a very good understanding of economic concepts.",
"has a good grasp over the subject matter and understands economic relationships well.",
"can assimilate difficult subject matter with ease and apply it effectively.",
"Needs to put in efforts to improve his/her concepts.",
],
"Application & reasoning": [
"applies economic concepts aptly to reasoning questions.",
"can relate theoretical concepts to real-world economic situations.",
"analyses economic issues logically and draws sound conclusions.",
"Needs to strengthen the application of concepts to unfamiliar questions.",
],
"Data & graphs": [
"can interpret tables, graphs and economic data effectively.",
"Analysis and interpretation of graphs has been done well.",
"Needs to practise interpreting scales, trends and changes in data.",
],
"Diagrams & terminology": [
"economic diagrams are well drawn and accurately labelled.",
"uses appropriate economic terminology while explaining concepts.",
"Needs to improve the accuracy and labelling of economic diagrams.",
"Needs to use economic terms more consistently in written responses.",
],
"Answer writing": [
"writes well-structured answers and supports explanations with relevant examples.",
"presents economic arguments clearly and logically.",
"Needs to read questions thoroughly and address all parts of the question.",
],
"Revision & improvement": [
"He needs to follow a structured study and revision plan to bridge the gaps evident in the assessment papers.",
"Regular revision of definitions, diagrams and application-based questions will strengthen his performance.",
"Solving previous years' papers is recommended.",
"With focus and concerted efforts, he is sure to excel in the subject.",
],
},
}
