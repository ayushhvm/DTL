import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Set page config
st.set_page_config(
    page_title="Cosmetics Recommender",
    page_icon="💄",
    layout="wide"
)

@st.cache_data
def load_data():
    """Load the required data and matrices"""
    # Load your saved data files
    data = pd.read_pickle('data.pkl')
    ingred_matrix = pd.read_pickle('ingred_matrix.pkl')
    return data, ingred_matrix

def recommender(search, data, ingred_matrix):
    """Modified recommender function to return results instead of printing"""
    cs_list = []
    brands = []
    output = []
    binary_list = []
    
    try:
        idx = data[data['product_name'] == search].index.item()
    except:
        return None, "Product not found in database"
    
    for i in ingred_matrix.iloc[idx][1:]:
        binary_list.append(i)    
    point1 = np.array(binary_list).reshape(1, -1)
    point1 = [val for sublist in point1 for val in sublist]
    
    prod_type = data['product_type'][data['product_name'] == search].iat[0]
    brand_search = data['brand'][data['product_name'] == search].iat[0]
    data_by_type = data[data['product_type'] == prod_type]
    
    for j in range(data_by_type.index[0], data_by_type.index[0] + len(data_by_type)):
        binary_list2 = []
        for k in ingred_matrix.iloc[j][1:]:
            binary_list2.append(k)
        point2 = np.array(binary_list2).reshape(1, -1)
        point2 = [val for sublist in point2 for val in sublist]
        dot_product = np.dot(point1, point2)
        norm_1 = np.linalg.norm(point1)
        norm_2 = np.linalg.norm(point2)
        cos_sim = dot_product / (norm_1 * norm_2)
        cs_list.append(cos_sim)
    
    data_by_type = pd.DataFrame(data_by_type)
    data_by_type['cos_sim'] = cs_list
    data_by_type = data_by_type.sort_values('cos_sim', ascending=False)
    data_by_type = data_by_type[data_by_type.product_name != search]
    
    l = 0
    for m in range(len(data_by_type)):
        brand = data_by_type['brand'].iloc[l]
        if len(brands) == 0:
            if brand != brand_search:
                brands.append(brand)
                output.append(data_by_type.iloc[l])
        elif brands.count(brand) < 2:
            if brand != brand_search:
                brands.append(brand)
                output.append(data_by_type.iloc[l])
        l += 1
    
    return pd.DataFrame(output)[['product_name', 'brand', 'product_type', 'cos_sim']].head(5), None

def main():
    st.title("🎯 Cosmetics Product Recommender")
    st.write("Find similar cosmetic products based on ingredients!")

    try:
        # Load data
        data, ingred_matrix = load_data()
        
        # Create sidebar with product type filter
        st.sidebar.header("Filters")
        product_types = sorted(data['product_type'].unique())
        selected_type = st.sidebar.selectbox(
            "Filter by Product Type",
            ["All"] + product_types
        )
        
        # Filter products based on selected type
        if selected_type != "All":
            filtered_products = data[data['product_type'] == selected_type]['product_name'].tolist()
        else:
            filtered_products = data['product_name'].tolist()
            
        # Create main search interface
        search_product = st.selectbox(
            "Select a product to find similar items:",
            filtered_products
        )
        
        if st.button("Find Similar Products"):
            with st.spinner("Finding similar products..."):
                results, error = recommender(search_product, data, ingred_matrix)
                
                if error:
                    st.error(error)
                else:
                    # Display original product info
                    st.subheader("Selected Product")
                    original_product = data[data['product_name'] == search_product].iloc[0]
                    st.write(f"**Brand:** {original_product['brand']}")
                    st.write(f"**Type:** {original_product['product_type']}")
                    
                    # Display recommendations
                    st.subheader("Recommended Products")
                    
                    # Format similarity scores as percentages
                    results['Similarity'] = (results['cos_sim'] * 100).round(1).astype(str) + '%'
                    
                    # Display results in a clean format
                    for _, row in results.iterrows():
                        with st.container():
                            st.markdown(f"""
                            ##### {row['product_name']}
                            - **Brand:** {row['brand']}
                            - **Product Type:** {row['product_type']}
                            - **Similarity Score:** {row['Similarity']}
                            """)
                            st.divider()
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please make sure all required data files are present in the app directory.")

if __name__ == "__main__":
    main()
