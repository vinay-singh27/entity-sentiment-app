import torch
from transformers import DistilBertTokenizer, DistilBertModel, DistilBertForSequenceClassification
from transformers import AutoTokenizer, AutoModelForTokenClassification


class PredictSentiment:

    def __init__(self):

        # QA model
        self.qa_tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased-distilled-squad')
        self.qa_model = DistilBertModel.from_pretrained('distilbert-base-cased-distilled-squad')

        # Entity model
        self.ner_tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
        self.ner_model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

        # Sentiment Model
        self.pn_tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
        self.pn_model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

    def predict(self, text):

        

    def predict(self, text):

        # create dataframe for the text
        tweet_dataframe = pd.DataFrame(data=[text], columns=['content'])

        # data cleaning
        processed_dataframe = self.data_processing(tweet_dataframe)

        # extract the clean text
        clean_text = processed_dataframe['Clean_text'].iloc[0]

        # extract the entities
        entity_df = self.extract_entities(clean_text)

        # extract dependent phrase for the entities
        entity_df = self.extract_entity_dependent_phrase(entity_df)

        # predict sentiment on the text
        sentiment_df = self.extract_roberta_sentiment(entity_df)

        string_result = []
        for idx, row in sentiment_df.iterrows():
            string_result.append(f"{row['Entity']}   ->   {row['Roberta_label']}")

        string_result = "\n".join(string_result)

        return string_result



    def data_processing(self, tweet_dataframe):
        """
        This method preprocess the input dataframe.
        The data cleaning pipeline can be controlled using
        the initializing variable
        :param tweet_dataframe: input dataframe
        :return: prepared_dataframe with added Clean_text column
        """

        tweet_dataframe['Clean_text'] = tweet_dataframe['content']
        tweet_dataframe['Clean_text'] = tweet_dataframe['Clean_text'].apply(
            lambda x: data_cleaning(x, **self.data_cleaning_params))

        # drop exact duplicate clean texts
        prepared_dataframe = tweet_dataframe.drop_duplicates(subset=['Clean_text'])

        return prepared_dataframe

    def extract_entities(self, clean_text):
        """
        This function uses spacy nlp pipeline to extract entities
        :param clean_text: string
        :return: dataframe with the list of all the entities in the clean_text
        """

        # identify the entities in the dataset
        entity_results = []
        doc = self.nlp(clean_text)
        for ent in doc.ents:
            entity_results.append([ent.text, ent.label_])

        # create dataframe of the entities
        entity_df = pd.DataFrame(data=entity_results, columns=['Entity', 'Type'])
        entity_df['Clean_text'] = clean_text

        return entity_df

    def extract_entity_dependent_phrase(self, dataframe):
        """
        This function uses trained NLP-QA model to extract
        the dependent phrase from the text for the entity
        :param dataframe:
        :return:
        """

        dataframe.reset_index(drop=True, inplace=True)
        results = []
        for idx, row in dataframe.iterrows():
            # create QA input
            qa_input = {'question': f"what do you think about {row['Entity']}",
                        'context': row['Clean_text']}

            # predict from the QA model
            res = self.nlp_qa(qa_input)
            result_qa_m = [res['answer'], res['score']]

            results.append(result_qa_m)

        results_df = pd.DataFrame(results, columns=['Answer', 'Answer_Score'])
        dataframe = pd.concat([dataframe, results_df], axis=1)
        dataframe = dataframe[dataframe['Answer_Score'] > 0.1]

        return dataframe

    def roberta_sentiment_analysis(self, text):
        """
        This function uses pre-trained RoBERTa sentiment
        analysis model to identify the whether the associated
        phrase with the sentiment is positive or negative.
        :param text:
        :return:
        """

        encoded_input = self.sa_roberta_tokenizer(text, return_tensors='pt')
        output = self.sa_roberta_model(**encoded_input)
        scores = output[0][0].detach().numpy()
        return softmax(scores)

    def extract_roberta_sentiment(self, dataframe):

        dataframe['Roberta_Polarity_Score'] = dataframe['Answer'].apply(lambda x: self.roberta_sentiment_analysis(x))

        # roberta labels
        dataframe['Roberta_Score'] = dataframe['Roberta_Polarity_Score'].apply(lambda x: x.max())
        dataframe['Roberta_label'] = dataframe['Roberta_Polarity_Score'].apply(lambda x: x.argmax())
        dataframe['Roberta_label'] = dataframe['Roberta_label'].map({0: 'Negative', 1: 'Neutral', 2: 'Positive'})

        return dataframe

    def predict_sentiment(self, text):
        """
        This function combines all the function above
        to extract & predict the sentiment for the
        entity present in the text
        :param text:
        :return:
        """

        
