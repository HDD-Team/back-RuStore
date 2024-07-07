from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
import faiss
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.document_loaders import CSVLoader
from prompts import prompt1,prompt2
import json
from pars import parse
from langchain.schema import AIMessage


local_llm = "qwen2"
llm = ChatOllama(model=local_llm, format="json", temperature=0)
embedding_model = HuggingFaceEmbeddings(model_name="cointegrated/rubert-tiny2")
prompt = ChatPromptTemplate.from_template(prompt2)


def llm_chain(question):
    """
    Функция для построения chain для вызова invoke
    :return: на выходе функция дает chain, который можно запускать с помощью invoke
    """

    db = FAISS.load_local(r"faiss_try1", embedding_model, allow_dangerous_deserialization=True)
    search_kwargs = {
        'k': 10,  # Number of nearest neighbors to retrieve
        'nprobe': 5,  # Number of clusters to explore
        'metric_type': faiss.IndexFlatL2,  # Use Euclidean distance  METRIC_L2
        'efSearch': 50,  # HNSW-specific parameter for search quality
        'max_dist': 0.5,  # Maximum distance for neighbors
    }
    retriever = db.as_retriever() #search_kwargs=search_kwargs
    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )
    result = chain.invoke(question)
    parsed_data = json.loads(result)
    link = "https://" + parsed_data.get("Link")
    print(result)
    print(link)
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(f"""Ты - бот для обслуживания разработчиков для приложения RuStore, аналог Google Play. Ты получаешь информацию для ответа из этой ссылки  {link}. Твой ответ должен быть следующего формата:
                         1. Ответ на вопрос пользователя.
                         2. Исправленный код в ```code``` если требуется."
                         3. Ссылка: """)
            ),
            HumanMessagePromptTemplate.from_template("{text}"),
        ]
    )
    messages = chat_template.format_messages(text=parse(link))
    response = llm(messages)
    json_content = response.content
    parsed_data = json.loads(json_content)
    response_final = parsed_data.get("answer") + " \n Ссылка на подробную информацию ниже. "
    print(response_final)
    return {
        "answer": response_final,
        "url": link
    }


