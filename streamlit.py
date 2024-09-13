import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Superstore!!!', page_icon=':bar_chart:', layout='wide')
st.title(':bar_chart: Superstore EDA')
st.markdown('<style>div.block-container{padding-top:2.3rem;}</style>', unsafe_allow_html=True)

# File uploader for user-uploaded files
fl = st.file_uploader(':file_folder: Upload a file', type=['csv', 'txt', 'xls', 'xlsx'])
if fl is not None:
    # If a file is uploaded, read it using pandas
    st.write(fl.name)
    df = pd.read_csv(fl, encoding='ISO-8859-1')

    # Convert 'Order Date' to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])

    col1, col2 = st.columns(2)

    # Getting min and max date from the DataFrame
    startdate = df['Order Date'].min()
    enddate = df['Order Date'].max()

    with col1:
        date1 = pd.to_datetime(st.date_input('Start Date', startdate))
    with col2:
        date2 = pd.to_datetime(st.date_input('End Date', enddate))
    
    if date1 and date2:
        df = df[(df['Order Date'] >= date1) & (df['Order Date'] <= date2)].copy()

    # Filters
    region = st.sidebar.multiselect('Choose your regions:', df['Region'].unique())
    df2 = df[df['Region'].isin(region)] if region else df

    state = st.sidebar.multiselect('Choose your states:', df2['State'].unique())
    df3 = df2[df2['State'].isin(state)] if state else df2

    city = st.sidebar.multiselect('Choose your cities:', df3['City'].unique())
    df4 = df3[df3['City'].isin(city)] if city else df3

    filtered_df = df4

    # Plots and Data Analysis
    with col1:
        st.subheader('Category Wise Sales')
        category_sales = filtered_df.groupby(by=['Category'], as_index=False)['Sales'].sum().reset_index()
        trace = go.Bar(x=category_sales['Category'], y=category_sales['Sales'], text=category_sales['Sales'], textposition='auto')
        data = [trace]
        layout = go.Layout(
            xaxis=dict(title='Category'),
            yaxis=dict(title='Sales')
        )
        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig)

    with col2:
        st.subheader('Region Wise Sales')
        region_sales = filtered_df.groupby(by=['Region'], as_index=False)['Sales'].sum()
        trace = go.Pie(
            labels=region_sales['Region'],
            values=region_sales['Sales'],
            hole=0.4,
        )
        data = [trace]
        layout = go.Layout(title='Sales by Region')
        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig)

    col1, col2 = st.columns(2)

    with col1:
        with st.expander('Category Sales Data'):
            st.write(category_sales[['Category', 'Sales']].style.background_gradient(cmap='Blues'))
            csv = category_sales.to_csv(index=False).encode('utf-8')
            st.download_button('Download Category Sales', data=csv, file_name='category_sales.csv', mime='text/csv')

    with col2:
        with st.expander('Region Sales Data'):
            st.write(region_sales.style.background_gradient(cmap='Oranges'))
            csv = region_sales.to_csv(index=False).encode('utf-8')
            st.download_button('Download Region Sales', data=csv, file_name='region_sales.csv', mime='text/csv')

    # Time Series Analysis
    filtered_df['month_year'] = filtered_df['Order Date'].dt.to_period('M')
    st.subheader('Time Series Analysis')
    filtered_month = filtered_df.groupby('month_year')['Sales'].sum().reset_index()
    trace = go.Scatter(
        x=filtered_month['month_year'].dt.strftime('%Y:%b'),
        y=filtered_month['Sales'],
        mode='lines',
        line=dict(color='orange', width=4)
    )
    data = [trace]
    layout = go.Layout(
        xaxis=dict(title='Month and Year', titlefont=dict(color='green'), tickfont=dict(color='orange')),
        yaxis=dict(title='Sales', titlefont=dict(color='green'), tickfont=dict(color='orange'))
    )
    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig)

    with st.expander('Time Series Analysis Data'):
        st.write(filtered_month.T.style.background_gradient(cmap='Oranges'))
        csv = filtered_month.to_csv(index=False).encode('utf-8')
        st.download_button('Download Time Series Data', data=csv, file_name='filtered_month.csv', mime='text/csv')

    # Sales Hierarchical View
    st.subheader('Sales Hierarchical View')
    fig3 = px.treemap(
        filtered_df,
        path=['Region', 'Category', 'Sub-Category'],
        color='Sub-Category',
        hover_data={'Sales': True}
    )
    fig3.update_layout(width=1200, height=600)
    st.plotly_chart(fig3)

    with st.expander('Sales Hierarchical View Data'):
        hierarchical_data = filtered_df[['Region', 'Category', 'Sub-Category', 'Sales']]
        st.write(hierarchical_data.T.style.background_gradient(cmap='Oranges'))
        csv = hierarchical_data.to_csv(index=False).encode('utf-8')
        st.download_button('Download Hierarchical View Data', data=csv, file_name='hierarchical_data.csv', mime='text/csv')

    # Segment Wise Sales
    col3, col4=st.columns(2)
    with col3:
        st.subheader('Segment Wise Sales')
        segment = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
        trace = go.Pie(
                labels=segment['Segment'],
                values=segment['Sales'],
                marker=dict(colors=['yellow','purple','orange'])
            )
        data = [trace]
        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig)
    with col4:
        st.subheader('Category Wise Sales')
        segment = filtered_df.groupby('Category')['Sales'].sum().reset_index()
        colors = px.colors.qualitative.Plotly
        trace = go.Pie(
                labels=segment['Category'],
                values=segment['Sales'],
                marker=dict( colors=colors )
            )
        data = [trace]
        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig)
else:
    st.warning('Please upload a file to proceed.')
