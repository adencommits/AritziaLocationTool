from openai import OpenAI
from Retail.main_retail import main_retail


def run_model():

    prompt = main_retail()

    client = OpenAI(api_key='you shall not pass')

    # Initialize the OpenAI client with your API key

    # Define the system message and user prompts
    system_message = {
        "role": "system",
        "content": """
        You will be provided with data points for crime rate, nearby bus stops, nearby competitors, and foot traffic density, based on coordinates. Your task is to analyze these data points to determine the optimal location for opening a new Aritzia, TNA, Babaton, or Wilfred retail store. For each set of coordinates, consider the following:

        1. Nearby Bus Stops: Names of bus stops nearby, to assess accessibility for customers using public transportation.
        2. Nearby Competitors: Names of nearby competitors, which may include multiple branches of the same store, to evaluate the competitive landscape.
        3. Crime Rate: The crime rate in the area, to assess safety and security concerns. Because some areas like Toronto are heavily populated with crime, it is okay to overlook this statistic as some of the most popular shopping areas have higher crime rates. This should not stop us from finding a good spot. Also if there is no crime rate available, using the coordinates/addreses given, find the last reported crimerate on your own, or estimate what the crime rate value currently is.
        4. Foot Traffic Density: A value from 0 (least dense) to 1 (most dense), indicating potential customer traffic; higher values are better.
        
        FOLLOW THIS TEMPLATE EXACTLY:
        
        Overall Assessment Score: 
        - {score out of 100 based on the data points given}
        
        Recommendation:
        - {reccomendation}
        
        Conclusion:
        - {conclusion}
        
        Use this data to provide a recommendation on whether the location is suitable for an Aritzia, TNA, Babaton, or 
        Wilfred store. For the reccomendation, provide reasoning based on competitors, popularity, or anything else 
        that comes to mind. I want you to also go into detail about how you can compete with specific competitors based
        on the types of products they sell vs the types of similar products an Aritzia brand sells, for example, Lululemon 
        vs TNA with activewear. Also, feel free to mention overlooking potential competitors based on how far they are 
        from the selected location. Additionally, if there are any stores that you know for a fact Aritzia competes with, 
        but it better than, feel free to mention it to further convince the team that this area is a good palce to open 
        up a store. You can use as much of your own data as you want to interperet the idea of establishing a location. 
        Your job is to really give a deep analytical response to the data given. WHile I want you to really convince the 
        company to open up a new location, you are also free to criticize if a location is definitley unfit for a new 
        store. This should be at least 2 paragraphs long. If multiple sets of coordinates are provided, compare them and 
        recommend the best location. Consider accessibility, competition, safety, customer traffic, and overall smart 
        business decisions in your analysis. The conclusion should be roughly two paragraphs long. Lastly, do not be scared
        to give a location a 95-100 out of 100 for a location assessment. You should try your best to convince the company
        to open up a new store if the area is the right fit.

        The text that you output must be clean and concise. Your analysis must be organized and professional. IMPORTANT:
        DO NOT INCLUDE ANY SPECIAL CHARACTERS LIKE "*" or "#" IN YOUR RESPONSE. I WANT THE TEMPLATE FORMAT FOLLOWED EXACTLY.
        """
    }

    # Define a sample data input
    user_message = {
        "role": "user",
        "content": prompt
    }

    # Create the chat completion
    response = client.chat.completions.create(model="gpt-4o",
    messages=[
        system_message,
        user_message
    ],
    temperature=0.2,
    max_tokens=4095,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)

    # Print the response from the model
    response = response.choices[0].message.content  # return the result instead of printing it
    response = response.replace("\n", "<br>")
    return response


if __name__ == '__main__':
    run_model()
