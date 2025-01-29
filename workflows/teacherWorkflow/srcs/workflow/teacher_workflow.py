from src.rag.index import build_index
from src.agents.analyzer_agent import AnalyzerAgent
from src.agents.teacher_agent import TeacherAgent
from src.agents.reviewer_agent import ReviewerAgent
from llama_index.core import Settings
from dotenv import load_dotenv

load_dotenv()

def main():
    # Initialize components
    index = build_index()
    analyzer = AnalyzerAgent()
    teacher = TeacherAgent()
    reviewer = ReviewerAgent()
    
    # User input
    query = input("Ask me a question: ")
    
    # Step 1: Analyze and refine query
    refined_query = analyzer.analyze(query)
    
    # Step 2: Retrieve RAG context
    retriever = index.as_retriever(similarity_top_k=2)
    context_nodes = retriever.retrieve(refined_query)
    context = "\n".join([n.text for n in context_nodes])
    
    # Step 3: Generate child-friendly response
    response = teacher.teach(refined_query, context)
    
    # Step 4: Review and finalize
    final_response = reviewer.review(response)
    
    print("\nFinal Answer:")
    print(final_response)

### ENTRYPOINT ###
if __name__ == "__main__":
    main()