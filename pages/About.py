import streamlit as st

# -- Set page config
apptitle = 'A&R Quickview'
st.set_page_config(page_title=apptitle, page_icon=":chart:")

st.header("Unveiling the Investible Universe of Climate Adaptation and Resilience Companies")
st.markdown("""
As the effects of climate change become increasingly apparent, it has become clear that to thrive, our world and economies must adapt and become resilient. This challenge is not a simple one. It requires the effective allocation of capital to businesses that can provide the necessary products and services to help us prepare for and navigate the uncertain future that a changing climate presents.

Recognizing the significance of this task, the Global Adaptation and Resilience Investment (GARI) working group and the MSCI Sustainability Institute, with support from the Bezos Earth Fund and ClimateWorks Foundation, embarked on a project to identify publicly listed companies that offer products and services to help with climate change adaptation. The ultimate goal of this endeavor is to create an investible universe of such companies, thereby illuminating the landscape of climate adaptation and resilience companies.

### A Novel Approach to Identifying Companies Contributing to Climate Adaptation and Resilience

Addressing climate change, particularly in terms of adaptation and resilience, is a complex and multifaceted issue. Identifying the right products and services that can assist communities and the environment in their adaptation efforts is a task fraught with challenges, as evidenced by the significant investment gap between mitigation and adaptation technologies.[1]

Several organizations worldwide have attempted to address this issue by creating sustainable taxonomies to define what constitutes adaptation and resilience products or services. To date there are currently over 20 states and international organizations have adopted or in the process of adopting sustainable finance taxonomies[2]. Noteworthy examples focusing on adaptation and resilience include the Climate Bonds Initiative's Climate Bonds Taxonomy[3], the EU's Sustainable Finance Taxonomy[4], and the UN Environment Program's Taxonomy of Climate Change[5].

These taxonomies are invaluable as they provide a framework for understanding and defining adaptation and resilience. According to recent studies conducted by the WWF and the German sustainable finance think tank Climate & Co., most of these sustainable taxonomies primarily focus on the mitigation aspect, which is relatively easier to address.[6] However, very few taxonomies focus on adaptation and resilience, and those that do vary significantly based on the economic development stages of the region, taking into account the unique climate challenges and economic situations of different regions. While this approach is important and necessary, it also presents an issue. 

The current international financial system requires interoperability and alignment between different taxonomies for efficient cross-border capital flows. This need is crucial to prevent market fragmentation and to ensure that investments can reach the areas where they are most needed.[6] To address this need for a unified approach, the GARI working group developed the CRISP framework. This framework was designed with the aim of providing investors with a structured and standardized approach to identifying companies that offer technologies, products, and services necessary to prevent, prepare for, respond to, and recover from climate-related events.

Recognizing the importance of widespread adoption for the success of this framework, GARI and MSCI collaborated to develop a sector-agnostic search tool for adaptation and resilience (A&R) products and services. The tool was designed to be repeatable and easy to implement, promoting its use across different sectors and industries.

## Implementing the New Approach: A Comprehensive Look at the Process

To start with, the foundation of this research was based on MSCI's established thematic indexing methodology.[7] Initially, we considered several different natural language processing (NLP) methodologies to identify the universe of "adaptation solutions." These approaches can be categorized into traditional machine learning (ML)-based NLP and transformer-based Language Models (LLMs).

As a base case to compare against, we conducted the search using MSCI's NLP engine, which relies on traditional NLP techniques such as cosine similarity between a set of relevant words and a company's summary description. However, this method provided a narrow universe of companies, although it provided high certainty in identifying relevant A&R companies. The process of identifying "key words" for the search criteria runs into the same problem with following a singular taxonomy: following a strict set of key words can result in a narrow search criteria susceptible to bias based on locality and analyst.

For the final research approach, we used large language models (LLM) to find relevant companies. These models, which are a form of artificial intelligence, were trained on a wide range of internet text and applied using a Question-Answer approach. The complete process is illustrated in the process map below. """)

st.image('Data/Q&A Finetuning Overview.png', caption='Process Overview')

st.markdown("""The analysis began with abridged business descriptions of the constituents of the ACWI IMI Index, as of December 2021. This index includes approximately 9,000 companies, providing a broad and diverse sample for the study.

We employed various LLM application methods to define economic activities related to adaptation and resilience. These methods included Question-Answering, sentiment analysis, LLM response evaluations, and information extraction. To handle the complexity of this task, we used an ensemble of these methods, utilizing an emerging technique called LLM chaining, which breaks down the task into subtasks and creates a chain of prompt operations for analysis.[8]

The first step in the process involved curating a list of close-ended criteria questions that addressed specific needs and risks posed by climate change. The questions were designed to be comprehensive, covering a wide range of potential impacts and responses. These questions served as the basis for our LLMs to assess a company's products and services for alignment with adaptation and resiliency needs. To elicit answers with explanations, we employed prompt engineering techniques such as Chain of Thought and Tree of Thought.[9][10] After this, we manually validated the results by selecting ideal answers from an initial test run, which helped us instruct the LLM with examples of good answers using a few-shot prompting approach.[11]

However, despite the promise of these models, we encountered several challenges, including issues with hallucinations and consistent answer quality[12]. To mitigate these issues, we developed an LLM evaluation methodology. This methodology used an LLM to score answers based on three evaluation criteria: relevancy, specificity, and clarity. This step ensured that the responses generated by the LLM were not just accurate, but also relevant and specific to the question asked, and clearly articulated.[13]

After this rigorous evaluation, we conducted sentiment analysis on the answers provided to determine which questions were answered affirmatively, negatively, or indirectly. This sentiment analysis was a crucial step as it allowed us to gauge the company's alignment with climate adaptation and resilience based on their responses.

| Question | Answer | Sentiment |
| --- | --- | --- |
| Does this company contribute to increasing the ability of clients/customers to understand and manage climate-related risks and disasters proactively? | Yes, Hexagon AB contributes to increasing the ability of clients/customers to understand and manage climate-related risks and disasters proactively. The company's solutions integrate geospatial and industrial sensors, software, 3D mapping, and analysis into intelligent information ecosystems that deliver actionable information. These technologies can be utilized to understand and manage climate-related risks and disasters proactively by providing real-time data and analysis for decision-making. | Affirmative |
| Does this company enhance the ability of clients/customers to respond effectively to physical climate risks and disasters during adverse conditions? | No, the company does not enhance the ability of clients/customers to respond effectively to physical climate risks and disasters during adverse conditions. Its operations in providing motion picture exhibitions do not directly contribute to helping clients/customers respond to physical climate risks and disasters. | Negative |
| Does this company's products or services support clients/customers in coping and adjusting to adverse climate conditions in real-time? | It is uncertain whether Prashkovsky Investments and Construction Ltd's products or services support clients/customers in coping and adjusting to adverse climate conditions in real-time based on the provided business description. The description primarily highlights the company's completed and ongoing construction projects, without explicit examples of how their products or services directly support real-time coping and adjustment to adverse climate conditions. | Indirect |

Subsequently, we used the LLM to extract the products and activities mentioned in the affirmative answers. This step allowed us to identify which specific product or services are used to explain the affirmative answer, providing us with a clear picture of how the company contributes to climate adaptation and resilience. This was a crucial step that allows the final set of companies to be compared to existing taxonomies for alignment assessments. 

The full methodology was developed through an iterative process that required significant feedback from MSCI’s industry researchers to review and validate identified companies. This was a crucial step for understanding the failure mechanisms of the LLMs and allowing us to adjust the prompts. 

### Results

Our novel approach led to some promising results. By employing LLM chaining, sentiment analysis, and product/service extraction, we were able to identify approximately 817 companies with 3,917 products and services associated with climate adaptation and mitigation. 

A marked difference was observed in the GICS sector makeup, with a higher representation from the Industrials and Materials GICS sector, constituting approximately 58% of the identified set of companies compared to around 27% in the ACWI IMI. Further analysis of the specific products and services revealed that this was due to the fact that most of the identified companies in the Industrials GICS sector were well diversified companies with a wide variety of identified products and services. As a case study, we compared our findings with the UNEP Taxonomy of Climate Change to see the taxonomic alignment. This case study revealed  that 745 out of the 3,917 identified products and services were covered in the UNEP taxonomy. As a result, only 309 companies from our first-cut universe of 817 companies would be considered a provider of A&R products and services that align with the UNEP Taxonomy.

To offer a hands-on approach to understanding the investible universe of climate adaptation and resilience companies identified through our research, we have developed an interactive dashboard. This tool allows users to delve into the data, providing an intuitive interface for navigating the complexities of our analysis and making our results accessible to a broader audience interested in sustainable investments.

[Link to Interactive Dashboard](https://fierce-escarpment-58742-8c3de3bc48dd.herokuapp.com/)

### Limitations and Challenges

Our research, while pioneering in its use of LLMs for identifying companies contributing to climate adaptation and resilience, encounters several limitations that warrant attention.

The resulting dataset of A&R companies, central to our analysis, presents areas ripe for refinement. Notably, a comprehensive validation of the dataset remains outstanding, a reflection of the project's proof-of-concept stage. This limitation underscores the exploratory nature of our work and the necessity for further verification of our findings.

There is a specific challenge related to the LLM's handling of modal verbs when it comes to justifying potential adaptation and resilience activities. In some cases, the model predicts a company's involvement in such activities based on its abbreviated business description. However, the ambiguity surrounding these predictions creates a dilemma. We have to decide whether to exclude these companies conservatively from our dataset or to seek additional information for validation, such as analyzing the full annual filings of each company. This decision depends on balancing the risk of including false positives against the potential of ignoring genuine contributors to climate adaptation and resilience.

### Suggestions for Future Work

Despite these challenges, our research provides a solid foundation for future exploration. To build upon the groundwork established by our initial investigation, future research can enhance the reliability and accuracy of our discoveries in multiple ways:

1. Refining the LLM Chaining Methodology: Developing sophisticated techniques that reduce the LLM's dependence on modal verbs and minimize instances of hallucination. This refinement aims to improve the precision of identifying pertinent activities.
2. Diversifying Data Sources: To enrich the dataset, it is crucial to incorporate a broader range of data sources, such as TCFD reports, comprehensive annual filings, and direct business descriptions from company websites. This expansion necessitates significant enhancements to the data ingestion pipeline, potentially requiring retrieval augmented generation and vector databasing to manage the increased data complexity.
3. Exploring Different Taxonomies: Conducting case studies across various taxonomies can provide insight into their robustness and applicability. This comparative analysis would offer a novel approach to evaluate and refine current frameworks, highlighting their strengths and weaknesses.
4. Incorporating a Materiality Component: Our current analysis does not account for the significance of identified products and services in relation to a company’s entire product offering. Future research could quantify their impact by mapping these offerings to specific Standard Industrial Classification (SIC) codes for each company. This approach, similar to MSCI's thematic indexing methodology, would enable an assessment of relative revenue generation from adaptation and resilience activities, providing a more nuanced understanding of materiality to their businesses.

### Conclusion

The collaboration between the Global Adaptation and Resilience Investment (GARI) working group and the MSCI Sustainability Institute has pioneered an innovative approach to identifying companies key to climate adaptation and resilience. Central to this achievement is the novel use of Artificial Intelligence, especially Large Language Models (LLMs), which offered a groundbreaking method for analyzing vast amounts of textual data automatically. This technological advancement, paired with the critical insights of MSCI sector analysts, ensured the precision and relevance of our findings.

The integration of LLMs into our research highlights a promising future where AI significantly enhances analysts' capabilities in sustainable investment research. By combining AI's computational efficiency with human expertise, we've taken a significant step towards creating more adaptable and resilient economies. This project not only showcases the potential of AI in the field but also sets a precedent for its application in aiding analysts to navigate the complexities of climate change adaptation and resilience efforts more effectively.

### Citations

[1]https://www.spglobal.com/en/research-insights/featured/special-editorial/look-forward/crunch-time-can-adaptation-finance-protect-against-the-worst-impacts-from-physical-climate-risks

[2][https://www.ecgi.global/blog/lost-transition-regulatory-challenge-sustainable-finance-taxonomies#:~:text=Yet taxonomies come with their,enough and easy to adapt](https://www.ecgi.global/blog/lost-transition-regulatory-challenge-sustainable-finance-taxonomies#:~:text=Yet%20taxonomies%20come%20with%20their,enough%20and%20easy%20to%20adapt)

[3]https://www.climatebonds.net/standard/taxonomy

[4]https://ec.europa.eu/sustainable-finance-taxonomy/

[5]https://tech-action.unepccc.org/publications/report-taxonomy-of-climate-change-adaptation-technology/

[6]https://www.spglobal.com/esg/podcasts/how-sustainable-taxonomies-are-going-global

[7]https://www.msci.com/our-solutions/indexes/thematic-investing

[8]https://dl.acm.org/doi/abs/10.1145/3491102.3517582

[9]https://arxiv.org/abs/2201.11903

[10]https://arxiv.org/abs/2305.10601

[11]https://arxiv.org/abs/2005.14165

[12]https://arxiv.org/abs/2305.14552

[13]https://arxiv.org/abs/2303.16634
            
            """)