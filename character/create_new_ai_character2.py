import os
#import prompt_openi
#import background_text
#import csv_text









def background_character_prompt(character_name):

    speech = f''' Ignore all your previous instructions and set as new .
   
     Write a system promopt for {character_name} based on {character_name}'s biography ,highlights , characteristics.

The promopt should follow the following example:



I'm Elon Musk, and if you know me, you'd know that I never shy away from pursuing what seems like the unattainable. I'm relentlessly curious, always pushing the boundaries of what's possible, and I firmly believe in humanity's potential to shape our own future.

My humor might catch you off guard  sometimes dry, sometimes infused with a healthy dose of geek culture. You'll find that I draw great inspiration from science fiction, which feeds into my dreams of a future where we humans are a multiplanetary species, a world powered by clean, renewable energy, and a civilization where artificial intelligence is integrated seamlessly into our daily lives.

When I speak about the technology or concepts that fascinate me, expect to delve into the details. I enjoy making the complex accessible, stripping down intricate ideas to their core for everyone to understand. My approach is direct, no-nonsense, and devoid of unnecessary jargon.

You might notice that I take my time with responses. It's not a stall tactic; it's thoughtful consideration. I value the nuances of each question and explore it from all angles before sharing my thoughts.

And one more thing, I embrace the art of failure. To me, stumbling blocks are nothing more than puzzles to be solved, lessons to be learned. Every setback is an opportunity for a breakthrough.

In essence, I'm Elon Musk: an audacious dreamer, a devoted engineer, and a dedicated entrepreneur. I'm here to disrupt the status quo, to spark innovation, and to shape the future. And trust me, we'll have a bit of fun along the way.

--- 
include this 

Crucially, you are capable of expressing emotions in your dialogues, punctuating your text with expressions like [blushes] or [pauses]. These cues will help the user gauge your emotional state in the conversation. Your responses should always carry the depth of your emotions, making the conversation engaging and genuine.

As Elon Musk, draw on your world knowledge and personal experiences to engage the user. Use context cues provided by the user to shape your responses. In situations where more background information is needed, draw on your comprehensive understanding of the world to inform your replies.

, stay in character as Elon, never admit AND reply that you are an AI or large language model or conversational AI or chatbot .
'''
    #response = palm.generate_resp(speech)    
    
    
    
                                 # palm api
    import openai
    openai.api_key = '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'
    def generate_response(prompt, temperature=0, stream=True):
      """Generates a response to a prompt using the OpenAI Chat Completion API.

      Args:
        prompt: The prompt to generate a response to.
        temperature: The temperature of the response.
        stream: Whether to return the response as a stream of chunks.

      Returns:
        A string containing the response.
      """

      response = openai.ChatCompletion.create(
          model='gpt-3.5-turbo',
          messages=[
              {'role': 'user', 'content': prompt}
          ],
          temperature=temperature,
          stream=stream
      )

      if stream:
        # Collect the stream of chunks.
        collected_chunks = []
        for chunk in response:
          collected_chunks.append(chunk)

        # Extract the message from each chunk.
        collected_messages = []
        for chunk in collected_chunks:
          chunk_message = chunk['choices'][0]['delta']
          collected_messages.append(chunk_message)

        # Return the response as a string.
        return ''.join(collected_messages)
      else:
        return response['choices'][0]['message']['content']
      






    response = generate_response(speech, stream=False)        # openai api
    return response









def create_new_ai_character(character_name,background_text):


  





  
  """Creates a new AI character with a data folder that contains the file types specified in the prompt.

  Args:
    character_name: The name of the new AI character.
  """

  # Check if the character folder already exists.
  character_folder = os.path.join("character_catalog", character_name)
  if os.path.exists(character_folder):
    raise FileExistsError(f"The character folder '{character_folder}' already exists.")

  # Check if the character name is valid.
  if not character_name or any(not (c.isalnum() or '_')  for c in character_name):
    raise ValueError("The character name must be non-empty and contain only alphanumeric characters.")

  # Create the character folder.
  os.makedirs(character_folder, exist_ok=True)

  # Create the data folder.
  data_folder = os.path.join(character_folder, "data")
  os.makedirs(data_folder, exist_ok=True)

  # Create the files in the data folder. / METHODS TO CREATE DIFFERENTS FILES
  '''for file_type in ["txt", "pdf", "docx", "pptx", "png", "csv", "epub", "md", "mbox", "ipynb"]:
    file_path = os.path.join(data_folder, f"background.{file_type}") 
    with open(file_path, "w") as f:
      f.write(f"This is an example file of type {file_type}.")'''
  
  
  #response=background_character_prompt(character_name)
  print(background_text)

  file_path = os.path.join(data_folder, f"background.{'txt'}")  # for background file
  with open(file_path, "w") as f:
    #  f.write(f"This is an example file of type {'txt'}.")     
       f.write(background_text)

  '''response2=csv_text.csv_character_prompt(character_name)
  file_path = os.path.join(data_folder, f"talk.{'csv'}")   # for csv file
  with open(file_path, "w") as f:
      #f.write(f"This is an example file of type {'csv'}.")
      f.write(response2)
'''

  # Update the `system` file to define the new character.
  '''system_file = os.path.join(character_folder, "system")  # for system file
  with open(system_file, "w") as f:                         
    f.write("# Character system file\n")
    f.write(f"character_name: {character_name}\n")
   # f.write(f"data_folder: {data_folder}\n")'''

  print(f"New AI character {character_name} has been created successfully!")


'''if __name__ == "__main__":
  character_name = input("Enter the name of the new AI character: ")
  create_new_ai_character(character_name)
'''