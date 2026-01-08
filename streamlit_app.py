# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Title
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input('Name On Smoothie')
st.write("The name on your smoothie will be", name_on_order)

# Get Snowflake session
cnx=st.connection("snowflake")
session = cnx.session()

# Load fruit options
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")

# Multiselect (up to 5)
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe.select("FRUIT_NAME").to_pandas()["FRUIT_NAME"].tolist(),
    max_selections=5
)

# Process selection
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')

    smoothiefroot_response = requests.get(
        "https://my.smoothiefroot.com/api/fruit/watermelon"
    )

    sf_df = st.dataframe(
        data=smoothiefroot_response.json(),
        use_container_width=True
    )


    # Build INSERT statement  ✅ (FIXED INDENTATION)
    my_insert_stmt = """ insert into smoothies.public.orders (ingredients, name_on_order)
        values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # Submit Order button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon='✅')

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)

import requests

smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)


sf_df = st.dataframe(
    data=smoothiefroot_response.json(),
    use_container_width=True
)

