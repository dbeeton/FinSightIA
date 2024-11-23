#DEPENDANCIES DETAILED BELOW
#pip install --upgrade pip
#pip install streamlit
#pip install pip install streamlit-option-menu
#pip install pandas_datareader
#pip install yfinance
#pip install pytickersymbols
#pip install seaborn
#pip install plotly
#pip install plotly_express
#pip install scipy
#pip install scikit-learn
#pip install stripe
#pip install Pillow
#pip install sendgrid
#pip install sqlite3

import os
import streamlit as st

st.set_page_config(layout="wide")

from streamlit_option_menu import option_menu

selected = option_menu(
    menu_title = "💎 FinSightIA", 
    options = ["Home","Investment Process", "Investment Objectives", "Stock Information", "Portfolio Optimisation Module","Place Trades - Pick a Platform"], 
        icons=['house-gear-fill','signpost', 'list-task', 'info', 'cpu', 'coin'], 
        menu_icon="none", 
        default_index=0,
        orientation = "horizontal",)

st.html(
	"<head> <!--	This website is a resource available to investors and financial advisors to better understand investment alternatives and gain assistance on the asset allocation decision and best platform to use to invest.  Note that past performance is an imperfect indication of future performance and this should not be considered to be financial advice but rather a useful tool contributing to the investment allocation decision.</head> -->"
)

if selected == "Home": 

	#Database Setup (SQLite) • Use SQLite to store user data, subscription status, and access permissions. • In app.py, initialize a simple SQLite database that records user information (e.g., email, subscription_status, and access_expiration). 
	import sqlite3 
	def initialize_database(): 
		conn = sqlite3.connect('users.db') 
		cursor = conn.cursor() 
		cursor.execute(''' 
			CREATE TABLE IF NOT EXISTS users ( 
				email TEXT PRIMARY KEY, 
				subscription_status TEXT, 
				access_expiration DATE 
			) 
		''') 
		conn.commit() 
		conn.close() 
	
	#Setting up Stripe • Create a Stripe account and set up a product and pricing for your paywall. • Generate a checkout session URL to direct users to a Stripe-hosted payment page. • Use Stripe’s API keys in your app and store them as environment variables in Streamlit Cloud.
	import stripe 
	import os 
	stripe.api_key = "sk_test_51QN6C6LmlMz4nhM3Kztut5CwKJ1Zv9o6B5mA42QOvP6sXsKKJBvmwqLev0Zjr5GhK9p5MVRoPg0Y5poofFX36Pdz001fYspjAz" # Load API key from environment 
	
	def create_checkout_session(email): 
		session = stripe.checkout.Session.create( 
			payment_method_types=['card'], 
			line_items=[{ 
				'price': 'price_1QN6FvLmlMz4nhM3Z3ahECh1', # Replace with Stripe's price ID for your product 
				'quantity': 1, 
			}], 
			mode='subscription', 
			success_url='https://your-app-url.streamlit.app/success?session_id={CHECKOUT_SESSION_ID}', 
			cancel_url='https://your-app-url.streamlit.app/cancel' 
		) 
		return session.url 

	#Streamlit App Setup • Build the Streamlit app to manage the user login, subscription status, and restricted content. • Allow users to log in using their email and check their subscription status from the SQLite database. • If the user is not subscribed, show the Stripe checkout link; otherwise, grant access to the premium content. 
	import streamlit as st 
	from datetime import datetime 
	import sqlite3 
	#Initialize login status in session state
	if 'is_logged_in' not in st.session_state:
		st.session_state['is_logged_in'] = False
	# Initialize the database 
	initialize_database() 
	# Login/Signup 
	st.subheader("Welcome to FinSight Information Assistant") 
	st.write("There are many financial advisors and investors who feel that they are searching for a needle in a haystack when it comes to selecting the best investments to match their requirements and risk profile.  It often just comes down to educated guesswork as there is so much qualitative financial information available which is often conflicting and dispersed. The aim of this product is to help making information available to financial advisors and their clients which identifies assets which match the clients investment preferences and objectives and then seek to construct the optimal portfolio.")
	st.write("")
	st.write("It should also be noted that FinSightIA does not receive any referral fees from ETF Managers or Investment Platform Providers and that all of the content on this site is focussed on supporting financial advisors and their clients in selecting the most appropriate investments and investment platforms.")
	st.write("In order to access the :blue[Stock Information] (identification of good value stocks which match your allocation preferences) and :blue[Portfolio Optimisation Module] (determining the optimal mix of assets based on asset return, volatility, correlation and other factors) you will need to subscribe for premium access at a cost of AUD150 per annum (:blue[refer to Investment Process page for examples of premium modules]).")

	email = st.text_input("Enter your email, :red[required for sign in and subscription]") 
	if st.button("Log In"): 
		conn = sqlite3.connect('users.db') 
		cursor = conn.cursor() 
		cursor.execute("SELECT subscription_status, access_expiration FROM users WHERE email = ?", (email,)) 
		user = cursor.fetchone() 
		if user: 
			subscription_status, access_expiration = user 
			if subscription_status == "active" and datetime.now() <= datetime.fromisoformat(access_expiration): 
				st.session_state['is_logged_in'] = True
				st.success("Access granted to premium content!") # Display premium content 
			else: 
				st.warning("Your subscription has expired. Please renew.") 
				checkout_url = create_checkout_session(email) 
				st.markdown(f"[Subscribe Here]({checkout_url})") 
		else: 
			st.info("Please subscribe to access premium content.") 
			checkout_url = create_checkout_session(email) 
			st.markdown(f"[Subscribe Here]({checkout_url})") 
			conn.close() 	

if selected == "Investment Process": 
	st.subheader(':red[Identifying Optimal Investments to deliver Investors Custom Strategy]') 
	from PIL import Image
	investment_process_img = Image.open("Investment_Process.jpg")
	st.image(investment_process_img)	
	
	#Link to examples of stock_info and portfolio optimiser tabs
	
	with open("Example_Stock_Info_Aus_Biotech_Alzheimer.pdf", "rb") as pdf_file:
		pdf_data = pdf_file.read()
		st.download_button(label="Download Stock Information Example", data=pdf_data, file_name="Example_Stock_Info_Aus_Biotech_Alzheimer.pdf", mime="application/pdf")

	with open("Example_Portfolio_Optimiser.pdf", "rb") as pdf_file:
		pdf_data = pdf_file.read()
		st.download_button(label="Download Portfolio Optimisation Module Example", data=pdf_data, file_name="Example_Portfolio_Optimiser.pdf", mime="application/pdf")
		
	st.subheader(':blue[Common frustrations for investors are:]') 
	#st.divider()
	col1, col2 = st.columns(2)

	with col1:
		with st.container(border=True):
			st.html("<h5>More sophisticated investor</h5>")
			st.write("If I know what types of returns/risks I want to be exposed to, how do I go about finding the right assets to invest in?")

	with col2:
		with st.container(border=True):
			st.html("<h5>Less sophisticated investor</h5>")
			st.write("I am not very knowledgeable about financial markets and I would like someone to just tell me what to invest in.")

	st.subheader(':blue[The portfolio optimisation module should assist both of these classes of user but it is important to note the following caveats:]')

	column1, column2, column3, column4 = st.columns(4)

	with column1:
		with st.container(border=True):
			st.html("<h5>No best portfolio that meets all investor requirements</h5>")
			st.write("There is a best portfolio given the individuals circumstances, existing assets and risk/return preferences.  The challenge is distilling information to find the investors best fit portfolio.")

	with column2:
		with st.container(border=True):
			st.html("<h5>Define goals before looking at investment options.</h5>")
			st.write("Spend the required time on each part of the investment process (don't skip any steps). Formulate your investment objectives and in particular your tolerance for adverse investment outcomes which may impact the asset classes and assets you invest in.")

	with column3:
		with st.container(border=True):
			st.html("<h5>High level sense test all critical inputs to the investment decision.</h5>")
			st.write("Particularly review the price data used in the portfolio optimisation module as there are occasional inaccuracies with the vendor provided data.")

	with column4:
		with st.container(border=True):
			st.html("<h5>The portfolio optimisation module is designed to assist financial advisors.</h5>")
			st.write(":red[There are many factors to consider in the investment strategy construction process and selection of investments to deliver on this.  Individual investors should not use the portfolio optimisation module in the absence of guidance from a financial advisor.]")
	
	with st.expander("It is important to understand the tax implications for your portfolio, particularly if you invest outside of Australia"):
		tax_implications = '''
		<div style='text-align: left;'>
		  <p style='color: blue;'>The below has been written from the perspective of an individual investor, for tax implications of investing through companies or trusts please seek specialist tax advice:</p>
		  <ul>
			<li>Australian Residents are taxed on dividends and capital gains of all assets (Australian and Foreign).</li>
			<li>Fully franked dividends (i.e. Company income taxed in Australia) will provide a 30% tax credit, no franking credit available for foreign company dividends.</li>
			<li>Some countries have a withholding tax on dividends (e.g. US = 15%) and some do not (e.g. UK). If withholding tax is deducted it can generally be claimed as a foreign tax offset against Australian tax payable.</li>
			<li>Foreign investment capital gains still qualify for the 50% CGT discount if held for >12 months. Offsets would generally apply for any CGT paid to foreign tax authorities (if applicable).</li>
			<li>These rules apply equally to ETFs (Exchange Traded Funds) for which administration is made easier by the provision of an annual statement with all required tax details.</li>
			<li>Australian investors are generally not required to lodge tax returns to foreign tax authorities.</li>
		  </ul>
		</div>
		'''
		st.components.v1.html(tax_implications, height=400)


if selected == "Investment Objectives":
	st.subheader(":red[Maximise Return per unit of risk for alternatives within your risk tolerance]")
	st.subheader(':blue[Investment Objectives]') 
	#st.divider()
	col1, col2, col3, col4 = st.columns(4)

	with col1:
		with st.container(border=True):
			st.html("<h5>Do worst case analysis</h5>")
			st.write("The disclaimer of past performance is no indication of future performance is commonly cited.  While there are some trends that are expected to continue to hold in the long run (e.g. Equity Markets outperforming bonds and cash) there can be significant deviations in the short term.")
	
	with col2:
		with st.container(border=True):
			st.html("<h5>Understand your risk vs reward tolerance</h5>")
			st.write("Academics would advocate maximising the return over the risk free rate against risk (volatility) but some investors may have different objectives.  Generally older and less wealthy investors demand lower variability of outcomes due to shorter investment horizons and increased sensitivity to losses respectively.")
	
	with col3:
		with st.container(border=True):
			st.html("<h5>Understand the benefits of the different allocation classes</h5>")
			st.write("The primary asset classes are Cash (& Bonds), Equities, Property and Commodities. Cash has the most certainty of outcomes but generally produces the lowest return in the long term.")

	with col4:
		with st.container(border=True):
			st.html("<h5>Don't forget the common sense test</h5>")
			st.write("Avoid putting all your eggs in one basket. Be cautious of strong performance by a few very large companies causing lack of diversification for value weighted ETFs. Note: Empirical evidence suggests that 1) small/medium cap stocks outperform large cap and, 2) value stocks outperform growth stocks and 3) Equally weighted ETFs outperform value weighted over the long term.")

	st.write("My advice to the trustee [of my will] could not be more simple: Put 10% of the cash in short-term government bonds and 90% in a very low-cost S&P 500 index fund. :red[Warren Buffet]")

	#st.divider()
	st.subheader(':blue[Advantages of ETFs (Exchange Traded Funds)]')
	#st.divider()
	col1, col2, col3, col4 = st.columns(4)

	with col1:
		with st.container(border=True):
			st.html("<h5>Easy to Trade</h5>")
			st.write("You buy and sell ETF units just like ordinary shares (e.g. CBA). They're listed on the ASX and can be bought through your existing brokerage account. Unlike most companies that have three character ticker codes, many ETFs have four or five character ticker codes.")
	
	with col2:
		with st.container(border=True):
			st.html("<h5>Wide Range of Strategies and Markets</h5>")
			st.write("All major corners of the market are now accessible to retail investors via ASX ETFs e.g. foreign markets, individual commodities and sectors.")
	
	with col3:
		with st.container(border=True):
			st.html("<h5>Diversified</h5>")
			st.write("One ETF unit purchase can provide exposure to an entire sector, commodity or market.")
	
	with col4:
		with st.container(border=True):
			st.html("<h5>Long or Short</h5>")
			st.write("Short Sell the market with ease and profit when the market is going down. But be very careful of short/bear strategies as long run returns tend to be positive.")

if selected == "Stock Information" and st.session_state['is_logged_in'] == False: 
	st.write("In order to access the :blue[Stock Information] (identification of good value stocks which match your allocation preferences) you will need to subscribe for premium access on the home page at a cost of AUD150 per annum (:blue[refer to Investment Process page for examples of premium modules]).")

if selected == "Stock Information" and st.session_state['is_logged_in'] == True: 

	#Below imports all exchange tickers as at 30 Sep 17
	import pandas as pd
	ticker_df = pd.read_csv("Yahoo_Tickers.csv")

	toggle_label = (
		"Find Description of my ticker"
		if st.session_state.get("StockInputOrFind", False)
		else "Find me stocks based on region/activity/description keyword/s"
	)
	toggle_value = st.session_state.get("StockInputOrFind", False)
	Ticker_or_Find = st.toggle(toggle_label, value=toggle_value, key = "StockInputOrFind")

	ticker_df.sort_values("Country", inplace=True)
	ticker_country_unique = ticker_df["Country"].unique().astype(str)
	ticker_country_unique_list = ticker_country_unique.tolist()
	#ticker_sectors_unique_list = ['Communication services', 'Consumer discretionary', 'Consumer staples', 'Energy', 'Financials', 'Healthcare', 'Industrials', 'Information technology', 'Materials', 'Real estate', 'Utilities']
	ticker_df.sort_values("Category Name", inplace=True)
	ticker_category_unique = ticker_df["Category Name"].unique().astype(str)
	ticker_category_unique_list = ticker_category_unique.tolist()

	if toggle_label == "Find me stocks based on region/activity/description keyword/s":
		Ticker_Country = st.multiselect("Ticker Country", ticker_country_unique_list)
		Ticker_Category = st.multiselect("Ticker Category", ticker_category_unique_list)
		Description_Filter_Phrase = st.text_input("Ticker Description Filter Phrase", "")
		reduced_ticker_df = ticker_df[ticker_df["Country"].isin(Ticker_Country)  == True]
		reduced_ticker_df = reduced_ticker_df[reduced_ticker_df["Category Name"].isin(Ticker_Category)  == True]
		reduced_ticker_df.sort_values(by = 'Ticker',  ascending=True, inplace = True)
		all_tickers = reduced_ticker_df['Ticker']. tolist()
		if 'clicked_stock' not in st.session_state:
			st.session_state.clicked_stock = False
	
		def click_button():
			st.session_state.clicked_stock = True
	
		st.button('Get Ticker Business Descriptions', on_click=click_button)
		
		if st.session_state.clicked_stock:
			search_text = []
			search_text = Description_Filter_Phrase.lower()
			matching_tickers = {}
			import yfinance as yf
			import pandas as pd
			business_summaries = {}
			ticker_match = []
			for t in all_tickers:
				stock = yf.Ticker(t)
				info = stock.info
				if 'longBusinessSummary' in info:
					business_summaries[t] = info['longBusinessSummary']
					ticker_match.append(t)
				else:
					continue
#					business_summaries[t] = "Summary not available"
			
			#Getting data from YFinance about a selected ticker
			import yfinance as yf
			selected_ticker_info = []
			selected_etf_info = []
			
			import math

			millnames = ['',' Thousand',' Million',' Billion',' Trillion']
			
			def millify(n):
				n = float(n)
				millidx = max(0,min(len(millnames)-1,
									int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
			
				return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
			
			for ticker in all_tickers:
				try:
					result = yf.Ticker(ticker).info
					if result['quoteType'] != 'ETF':
						stock_items = [result['symbol'], result['longName'], result['sector'], result['industry'], result['currency'], result['currentPrice'], millify(result['marketCap']), result['trailingPE'], result['forwardPE']]
						selected_ticker_info.append(stock_items) 
					else:
						continue
				except Exception as e:
					print(f"Failed to retrieve data for {ticker}: {e}") 
					
			selected_ticker_info_df = pd.DataFrame(selected_ticker_info, columns=['symbol', 'longName', 'sector', 'industry', 'currency', 'currentPrice', 'marketCap', 'trailingPE', 'forwardPE'])
			
			st.write(":blue[Below is a list of stocks in the region and category/industry selected, ordered by PE ratio. A low PE ratio could be indicative of good value.]")
			selected_ticker_info_df.sort_values(by = 'forwardPE',  ascending=True, inplace = True)
			st.dataframe(selected_ticker_info_df, hide_index=True)
			st.write("In simple terms, a good P/E (Price divided by Earnings) ratio for an established company is lower than 20 (average across regions and industries is usually 20-25). When looking at the P/E ratio alone, the lower it is, the better.  It is however more meaningful to compare P/E Ratio for a stock to the average of the sector/industry from which it derives the majority of its income.  Also note that it is difficult to set guidelines for startups where future earnings are quite uncertain.")

			st.write(":blue[Business descriptions for stocks in the region and category/industry selected are provided below where available]")

			# Print the summaries
			for ticker, summary in business_summaries.items():
				if search_text in summary.lower():
					st.write(f"Ticker: {ticker}")
					st.write(f"Business Summary: {summary}")
					st.write("\n" + "="*74 + "\n") #Separator for readability
				else:
					continue
					
			if st.session_state.clicked_stock == True:
				st.divider()
				st.write("To see relative returns and volatilities of tickers with descriptions copy these tickers into the Portfolio Optimisation Module as a Custom Ticker List:")
				for item in ticker_match:
					st.write(item)
				st.divider()
				st.write("To see relative returns and volatilities of all tickers matching the search copy these tickers into the Portfolio Optimisation Module as a Custom Ticker List:")
				for matchitem in all_tickers:
					st.write(matchitem)
			
			st.session_state.clicked_stock = False
	else:
		StockTicker = st.text_input("Input Stock or ETF ticker, note supplement with .Exchange code e.g. CBA.AX: ")
				
		import yfinance as yf
		selected_ticker_info = []
		selected_etf_info = []
			
		import math

		millnames = ['',' Thousand',' Million',' Billion',' Trillion']
		
		def millify(n):
			n = float(n)
			millidx = max(0,min(len(millnames)-1,
								int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
		
			return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
			
		try:
			result = yf.Ticker(StockTicker).info
			if result['quoteType'] != 'ETF':
				stock_items = [result['symbol'], result['longName'], result['sector'], result['industry'], result['currency'], result['currentPrice'], millify(result['marketCap']), result['trailingPE'], result['forwardPE']]
				selected_ticker_info.append(stock_items) 
			else:
				pass
		except Exception as e:
			print(f"Failed to retrieve data for {StockTicker}: {e}") 
				
		selected_ticker_info_df = pd.DataFrame(selected_ticker_info, columns=['symbol', 'longName', 'sector', 'industry', 'currency', 'currentPrice', 'marketCap', 'trailingPE', 'forwardPE'])
		
		st.write(":blue[Below is some key market data for the selected stock. A low PE ratio could be indicative of good value.]")
		selected_ticker_info_df.sort_values(by = 'forwardPE',  ascending=True, inplace = True)
		st.dataframe(selected_ticker_info_df, hide_index=True)
		st.write("In simple terms, a good P/E (Price divided by Earnings) ratio for an established company is lower than 20 (average across regions and industries is usually 20-25). When looking at the P/E ratio alone, the lower it is, the better.  It is however more meaningful to compare P/E Ratio for a stock to the average of the sector/industry from which it derives the majority of its income.  Also note that it is difficult to set guidelines for startups where future earnings are quite uncertain.")

		def getstockinfo(Stock_Ticker):
			import yfinance as yf
			stock = yf.Ticker(Stock_Ticker)
			return stock.info['longBusinessSummary']	
		st.divider()
		st.markdown("The description of " + StockTicker + " is : ")		
		if StockTicker == "":
			st.write("Please select a ticker")
		else:	
			Stock_Desc = getstockinfo(StockTicker)			
			html_str = f"""
			<style>
			p.a {{
			  font: 15px Courier;
			}}
			</style>
			<p class="a">{Stock_Desc}</p>
			"""		
			st.markdown(html_str, unsafe_allow_html=True)	

if selected == "Portfolio Optimisation Module" and st.session_state['is_logged_in'] == False: 	
	st.write("In order to access the :blue[Portfolio Optimisation Module] (determining the optimal mix of assets based on asset return, volatility, correlation and other factors) you will need to subscribe for premium access on the home page at a cost of AUD150 per annum (:blue[refer to Investment Process page for examples of premium modules]).")

if selected == "Portfolio Optimisation Module" and st.session_state['is_logged_in'] == True: 

	if "update_strategy" in st.session_state:
		st.session_state.update_strategy = st.session_state.update_strategy
	
	html_code = """<h3 style='color: red;'>
	  Assisting investors with their listed asset allocations
	</h3>"""
	st.markdown(html_code, unsafe_allow_html=True)
	##DISPLAY UNIVERSE OF AUSTRALIAN ETFs
	
	st.html("<h5>Universe of Australian Stock Exchange ETFs</h5>")
	#Below imports meta data for all ASX ETFs as at 31 Jul 24
	import pandas as pd
	etf_detail_df = pd.read_csv("ETF_Details.csv")
	
	#Displaying a sample of ASX ETF Meta Data to provide context
	st.write("Below is a summary with key details of all ASX ETFs, :blue[double click on cells in the table to see all content.]")
	st.dataframe(etf_detail_df, hide_index=True)
	
	##SELECTION OF REGIONS, STRATEGIES OR STOCKS BY USER
	
	st.html("<h5>Select Strategy or Stocks/ETFs</h5>")
	
	toggle_label = (
		"Minimum Fee ETF"
		if st.session_state.get("CustOrMin", False)
		else "Custom Tickers"
	)
	toggle_value = st.session_state.get("CustOrMin", False)
	Custom_or_MinFee = st.toggle(toggle_label, value=toggle_value, key = "CustOrMin")
	
	if toggle_label == "Minimum Fee ETF":
		Portfolio_Regions = st.multiselect("Portfolio Regions", ["Australia","Commodities","Europe","Ex_Australia","Ex_US_and_Canada","Global","United States"])
		Portfolio_Strategies = st.multiselect("Portfolio Strategies", ["Bear_Market","Broad","Cash_Bonds","Cash_Bonds_Currencies","Energy","Fixed_Interest","Gold","Index_Track","Mid_Cap","Narrow","NASDAQ","Palladium","Platinum","Property","Silver","Small_Cap","SP_500","Yield"])
	else:
		CustomTickerList = st.text_area("Enter Stock or ETF ticker")
		Custom_Ticker_list = [item.strip() for item in CustomTickerList.split()]
	
	##OUTPUT THE ETFs TO BE INCLUDED IN TARGET POTFOLIO (NEED TO PUT IN AN IF TO ONLY DO THE FOLLOWING IF ABOVE VAUES ARE CAPTURED)
	
	#For minimum fee optimisation approach select ETFs which have the minimum fee
	etf_detail_df_temp = etf_detail_df.copy()
	etf_detail_df_temp = etf_detail_df_temp.groupby(['Strategy', 'Region'])['Mgmt_Fee'].min().reset_index()
	etf_detail_df_temp = pd.merge(etf_detail_df_temp, etf_detail_df, on=['Strategy', 'Region', 'Mgmt_Fee'], how='inner')
	etf_detail_df_temp = etf_detail_df_temp.drop_duplicates(ignore_index= True)
	#etf_detail_df_temp
	
	#Identifing the ETFs to be optimised
	if toggle_label == 'Custom Tickers':
		etf_detail_df_temp = etf_detail_df[etf_detail_df["ASX_Code"].isin(Custom_Ticker_list)  == True]
	else:
		etf_detail_df_temp = etf_detail_df_temp[etf_detail_df_temp["Region"].isin(Portfolio_Regions)  == True]
		etf_detail_df_temp = etf_detail_df_temp[etf_detail_df_temp["Strategy"].isin(Portfolio_Strategies)  == True]	
	
	st.write("The following ETFs have been included in your custom portfolio, single stocks selected will also be included in analysis")
	st.dataframe(etf_detail_df_temp, hide_index=True)
	
	##LOAD UP THE TICKER PRICES FOR YAHOO FINANCE
	
	#Identifing the list of ETFs/Stocks to be optimised
	import pandas as pd
	GenTickers = [item.strip() for item in etf_detail_df_temp['ASX_Code']]
	if toggle_label == 'Custom Tickers':
		ETFTickers = (GenTickers + list(set(Custom_Ticker_list) - set(GenTickers)))
	else:
		ETFTickers = GenTickers
	
	#Define the base currency for calculation of indexed prices abd returns
	base_currency = st.selectbox("Base currency for calculation of indexed prices and returns", ["AUD","EUR","GBP","USD"], placeholder="AUD")
	
	#Enable users to capture return adjustments
	adjust_returns = st.checkbox("Tick this box if you would like to adjust returns")

	if adjust_returns:
		user_input = {}
		st.write("Enter return adjustments by ticker, note -0.01 means reduce annual return by 1% (0.00 means no adjustment)")
		for t in ETFTickers:
			user_input[t] = st.number_input(f"Enter return adjustment for {t}", value=0.0)
		return_adjustment_df = pd.DataFrame([user_input])
		return_adjustment_df = return_adjustment_df/252
		try:
			return_adjustment_df = return_adjustment_df.to_dict(orient='records')[0]
		except:
			st.write("Please select Stocks/ETFs and click :red[Run analysis on selection]")
		st.write("Daily return adjustments to be applied are below")
		st.write(return_adjustment_df)
	else:
		st.write("Returns will not be adjusted")	
	
	if 'clicked' not in st.session_state:
		st.session_state.clicked = False
	
	def click_button():
		st.session_state.clicked = True
	
	st.button('Run analysis on selection', on_click=click_button)
	
	if st.session_state.clicked:
	
		#Loading the historic price details for the ETFs/Stocks to be optimised
		import yfinance as yf 
		import pandas as pd 
		def get_stock_data_in_base(tickers):
			""" Fetches stock price data for a list of tickers in various currencies and converts them to AUD. 
			Parameters: 
			- tickers: List of stock tickers. 
			- currencies: Dictionary where keys are tickers and values are their respective local currencies. 
			- start_date: Start date for the price data. 
			- end_date: End date for the price data. Returns: - DataFrame with stock prices in AUD. """ 
		# Dictionary to store each stock's data converted to AUD 
			data_in_base = {} 
			
			for ticker in tickers: 
				try:
					# Get the currency for this ticker 
					stock = yf.Ticker(ticker)
					currency = stock.info["currency"]
			
					# Download historical price data for the ticker 
					stock_data = yf.download(ticker, period="max", progress=False)['Adj Close'] 
			
					# If currency is already AUD, no conversion needed 
					if {currency} == {base_currency}: 
						stock_data_base = stock_data
					else: 
						# Get the exchange rate from the stock's currency to AUD 
						fx_ticker = f"{currency}{base_currency}=X" # Ticker format for currency pairs in Yahoo Finance 
						fx_data = yf.download(fx_ticker, period="max", progress=False)['Adj Close'] 
			
						#Align the exchange rate data with stock data (reindex to match dates)
						fx_data = fx_data.reindex(stock_data.index).ffill().bfill()
						
						# Convert stock price to AUD by multiplying with the FX rate (assuming price is in the foreign currency) 
						stock_data_base = stock_data * fx_data 
	
					# Add the AUD converted data to the dictionary 
					data_in_base[ticker] = stock_data_base 
				except:
					pass					

			# Combine all tickers into a single DataFrame 
			close_price_df_tpd = pd.DataFrame(data_in_base) 

			return close_price_df_tpd 
		
		try:		
			close_price_df_tpd = get_stock_data_in_base(ETFTickers) 
			
			#If prices are missing for a given date then keep the price the same as the previous business day
			#close_price_df_tpd.update(close_price_df_tpd.iloc[:, 0:].replace([0,'0'], np.nan).ffill())
			close_price_df_tpd.sort_index(inplace=True)
			close_price_df_tpd = close_price_df_tpd.mask(close_price_df_tpd==0).ffill()
			#st.dataframe(close_price_df_tpd)
		except:
			st.session_state.clicked = False
			st.write("Please click :red[Run analysis on selection] once options have been selected")
			
		
		##NOW WE MAKE THE CALIBRATION DECISIONS
		
		st.write(":red[Defaults have been used to perform the initial run. Please change selections to match you preferences and click - Run analysis on selection above.  Note only assets which have price data for the full date range will be included in the analysis.]")
		
		st.html("<h5>Date range to use for base returns and correlation</h5>")
		st.write("Ideally you should include a full economic cycle in the date range")
		
		import datetime as dt
		from dateutil.relativedelta import relativedelta
		
		five_yrs_ago = dt.datetime.now() - relativedelta(years=5)
		start_calibration_date = st.date_input("Start of calibration window", min_value = dt.date(2007, 1, 1), value=five_yrs_ago)
		end_calibration_date = st.date_input("End of calibration window", value="default_value_today")
		
		MinCalDate = dt.datetime.combine(start_calibration_date, dt.time.min)
		MaxCalDate = dt.datetime.combine(end_calibration_date, dt.time.min)
		
		st.html("<h5>Investment details and risk free hurdle rate</h5>")
		
		initial_investment = st.number_input("Dollar amount you are looking to invest", value=1000000, step=100000)
		investment_horizon = st.number_input("Investment Horizon in Years", value=5, step=1)
		Risk_Free_Rate = st.number_input("Enter the current risk free rate", value = 0.04)
		number_of_sims = st.number_input("Number of Random Portfolio Weights to run", min_value = 1000, max_value=5000, step=1000)
		
		##ONLY RETAIN THE PRICE DATA FOR THE CALIBRATION WINDOW AND CHART PERFORMANCE OVER CAL WINDOW
		
		import datetime as dt
		from datetime import date
		#Determining the start date and end date for calibration window
		try:
			#Determining the start date and end date for calibration window and only include stock price dates in that range
			close_price_df_tpd['Date'] = close_price_df_tpd.index
			etf_price_calwindow_df = close_price_df_tpd[close_price_df_tpd["Date"].between(MinCalDate, MaxCalDate)]
			#Excluding ETFs/Stocks for which insufficient data is available to calibrate
			valid_columns = etf_price_calwindow_df.loc[MinCalDate].notna()
			etf_price_calwindow_df = etf_price_calwindow_df[valid_columns[valid_columns].index]
			close_price_df = etf_price_calwindow_df
			close_price_df.drop(['Date'], axis=1, inplace=True)
			close_price_df.sort_index(inplace=True)
			#st.dataframe(close_price_df)
			
			##Display scaled price to show relative performance of assets
			
			st.html("<h5>Scaled prices starting at 1 at the beginning of the calibration window</h5>")
			st.write("Prices are adjusted close price which is the closing price after adjustments for all applicable splits and dividend distributions. Data is adjusted using appropriate split and dividend multipliers, adhering to Center for Research in Security Prices (CRSP) standards.  Also note that all prices have been converted to ", base_currency," to reflect consistent ", base_currency," return outcomes.")
			# Function to scale stock prices based on their initial starting price
			# The objective of this function is to set all prices to start at a value of 1 
			def price_scaling(raw_prices_df):
				scaled_prices_df = raw_prices_df.copy()
				for i in raw_prices_df.columns[0:]:
					  scaled_prices_df[i] = raw_prices_df[i]/raw_prices_df[i].iloc[0]
				return scaled_prices_df
			
			price_scaling(close_price_df)
			scaled_price_df = price_scaling(close_price_df)
			#st.dataframe(scaled_price_df)
			
			if adjust_returns:
				#Create a copy of the scaled_price_df to enable replacement of numerical index with date index post normal transformations
				scaled_price_df_tmp = scaled_price_df.copy()
				
				#Restructure scaled_price_df to replace date index with 0 offset numerical index
				scaled_price_df.reset_index(inplace=True)
				scaled_price_df.rename(columns={"index": "Date"}, inplace=True)
				scaled_price_df.drop('Date', axis=1, inplace=True)
				
				#Calculate numerical returns and pick up adjustments to numerical returns (note adjustments are daily return adj)
				normalised_returns = scaled_price_df.select_dtypes(include=['number']).pct_change().fillna(0)
				
				#Apply the return adjustments to the returns over the calibration window
				try:
					for col in scaled_price_df.columns:
						if col in return_adjustment_df:
							normalised_returns[col] += return_adjustment_df[col]
				except KeyError as e:
					print(f"KeyError: {e} - Column might be missing in the DataFrame")
				
				#Create a frame for the population of the adjusted normalised prices, starting with 1 at t0
				adj_normalised_prices = pd.DataFrame(index=scaled_price_df.index, columns=scaled_price_df.columns)
				adj_normalised_prices.iloc[0] = 1
				
				#Calculate the adjusted normalised prices
				for i in range(1, len(scaled_price_df)):
					for col in scaled_price_df.columns:
						adj_normalised_prices.at[i, col] = adj_normalised_prices.at[i-1, col] * (1 + normalised_returns.at[i, col])
				
				#Replace the scaled_price_df and numerical index with the date index
				adj_normalised_prices.index = scaled_price_df_tmp.index
				scaled_price_df = adj_normalised_prices.copy()
			
			import matplotlib.pyplot as plt
			import seaborn as sns
			import plotly.express as px
			def plot_financial_data(df, title):
				
				fig = px.line(title = title)
				
				# For loop that plots all stock prices in the pandas dataframe df
				# Note that index starts with 1 because we want to skip the date column
				
				for i in df.columns[0:]:
					fig.add_scatter(x = df.index, y = df[i], name = i)
					fig.update_traces(line_width = 5)
					fig.update_layout({'plot_bgcolor': "white"})
			
				st.plotly_chart(fig)
				
			plot_financial_data(scaled_price_df, 'Start date indexed price through time (Start Calibration Date = 1)')
			
			#This produces the mean annual return of ETFs/Stocks over the calibration window
			scaled_return_df = scaled_price_df.pct_change(periods=1).fillna(0)
			
			import pandas as pd
			import numpy as np
			
			mean_annual_return = scaled_return_df.mean() * 252
			df_return = mean_annual_return.to_frame('Return')
			df_return['Return'] = df_return['Return']*100
			
			#This produces the standard deviation of ETF/Stock returns
			scaled_return_df = scaled_price_df.pct_change(periods=1).fillna(0)
			
			stddev = scaled_return_df.std() * np.sqrt(252)
			df_stdev = stddev.to_frame('Volatility')
			df_stdev['Volatility'] = df_stdev['Volatility']*100
	
			asset_return_risk_df = pd.merge(df_return, df_stdev, left_index=True, right_index=True)
			asset_return_risk_df = asset_return_risk_df.sort_index()
			asset_return_risk_df_form = asset_return_risk_df.style.format({
				'Return': '{:.2f}%'.format,
				'Volatility': '{:.2f}%'.format,
			})
			st.write("Below are the mean annual returns and volatilities of ETFs/Stocks over the calibration window: ")
			st.write(asset_return_risk_df_form)
			
			#This produces the correlation matrix for ETF/Stock returns, low correlation would indicate good diversification opportunities
			
			st.write("Below is the matrix of return correlations between selected assets: ")	
			
			scaled_return_df = scaled_price_df.pct_change(periods=1).fillna(0)
			
			import pandas as pd
			import numpy as np
			
			rs = np.random.RandomState(0)
			df = pd.DataFrame(rs.rand(10, 10))
			corr = scaled_return_df.corr()
			st.write(corr.style.background_gradient(cmap='coolwarm'))
			# 'RdBu_r', 'BrBG_r', & PuOr_r are other good diverging colormaps
			
			##RUN THE MONTE CARLO SIM TO IDENTIFY OPTIMAL PORTFOLIO ALLOCATION
			
			#This is the ensure that the list of weights that gets produced is combined with the ETFs/Stocks in the correct final sequence after all of the above data manipulation
			etf_list = close_price_df.columns.tolist()
			
			# Let's create an array that holds random portfolio weights
			# Note that portfolio weights must add up to 1 
			import random
			import numpy as np
			
			def generate_portfolio_weights(n):
				weights = []
				for i in range(n):
					weights.append(random.random())
					
				# let's make the sum of all weights add up to 1
				weights = weights/np.sum(weights)
				return weights
			
			# Assume that we have $1,000,000 that we would like to invest in one or more of the selected stocks
			# Let's create a function that receives the following arguments: 
				  # (1) Stocks closing prices
				  # (2) Random weights 
				  # (3) Initial investment amount
			# The function will return a DataFrame that contains the following:
				  # (1) Daily value (position) of each individual stock over the specified time period
				  # (2) Total daily value of the portfolio 
				  # (3) Percentage daily return 
			
			def asset_allocation(df, weights, initial_investment):
				portfolio_df = df.copy()
			
				# Scale stock prices using the "price_scaling" function that we defined earlier (Make them all start at 1)
				scaled_df = df
			  
				for i, stock in enumerate(scaled_df.columns[0:]):
					portfolio_df[stock] = scaled_df[stock] * weights[i] * initial_investment
			
				# Sum up all values and place the result in a new column titled "portfolio value [$]" 
				# Note that we excluded the date column from this calculation
				portfolio_df['Portfolio Value [$]'] = portfolio_df[0:].sum(axis = 1, numeric_only = True)
				portfolio_df.update(portfolio_df.iloc[:, 0:].replace([0,'0'], np.nan).ffill())
						
				# Calculate the portfolio percentage daily return and replace NaNs with zeros
				portfolio_df['Portfolio Daily Return [%]'] = portfolio_df['Portfolio Value [$]'].pct_change(1) * 100 
				portfolio_df.replace(np.nan, 0, inplace = True)
				
				return portfolio_df
			
			# Let's obtain the number of stocks under consideration (note that we ignored the "Date" column) 
			n = len(close_price_df.columns)
			
			# Let's define the simulation engine function 
			# The function receives: 
				# (1) portfolio weights
				# (2) initial investment amount
			# The function performs asset allocation and calculates portfolio statistical metrics including Sharpe ratio
			# The function returns: 
				# (1) Expected portfolio return 
				# (2) Expected volatility 
				# (3) Sharpe ratio 
				# (4) Return on investment 
				# (5) Final portfolio value in dollars
			import numpy as np
			
			def simulation_engine(weights, initial_investment):
				# Perform asset allocation using the random weights (sent as arguments to the function)
				portfolio_df = asset_allocation(scaled_price_df, weights, initial_investment)
			  
				# Calculate the return on the investment 
				# Return on investment is calculated using the last final value of the portfolio compared to its initial value
				return_on_investment = ((portfolio_df['Portfolio Value [$]'].iloc[-1:] - 
										 portfolio_df['Portfolio Value [$]'].iloc[0])/ 
										 portfolio_df['Portfolio Value [$]'].iloc[0]) * 100
			  
				# Daily change of every stock in the portfolio (Note that we dropped the date, portfolio daily worth and daily % returns) 
				portfolio_daily_return_df = portfolio_df.drop(columns = ['Portfolio Value [$]', 'Portfolio Daily Return [%]'])
				portfolio_daily_return_df = portfolio_daily_return_df.pct_change(periods=1).fillna(0)
			
				#Adjust mean returns (if they are believed to be unrepresentative of expected future performance, the below example adjusts a single ETF return by 5%)
				#portfolio_daily_return_df['VGS.AX'] = portfolio_daily_return_df['VGS.AX'] - 0.05/252
				
				# Portfolio Expected Annual Return formula
				expected_portfolio_return = np.sum(weights * portfolio_daily_return_df.mean() ) * 252
			  
				# Portfolio volatility (risk) formula
				# The risk of an asset is measured using the standard deviation which indicates the dispertion away from the mean
				# The risk of a portfolio is not a simple sum of the risks of the individual assets within the portfolio
				# Portfolio risk must consider correlations between assets within the portfolio which is indicated by the covariance 
				# The covariance determines the relationship between the movements of two random variables
				# When two stocks move together, they have a positive covariance when they move inversely, the have a negative covariance 
			
				covariance = portfolio_daily_return_df.cov().fillna(1/252) * 252 
				expected_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance, weights)))
			
				# Check out the chart for the 10-years U.S. treasury at https://ycharts.com/indicators/10_year_treasury_rate
				#rf = 0.03 # This should be parameterised to be maintained as rates move around
			
				# Calculate Sharpe ratio
				sharpe_ratio = (expected_portfolio_return - Risk_Free_Rate)/expected_volatility 
				return expected_portfolio_return, expected_volatility, sharpe_ratio, portfolio_df['Portfolio Value [$]'][-1:].values[0], return_on_investment.values[0]
			   
			# Set the number of simulation runs
			sim_runs = number_of_sims
			#initial_investment = float(input('Please input the amount to be invested in AUD: '))
			
			# Placeholder to store all weights
			weights_runs = np.zeros((sim_runs, n))
			
			# Placeholder to store all Sharpe ratios
			sharpe_ratio_runs = np.zeros(sim_runs)
			
			# Placeholder to store all expected returns
			expected_portfolio_returns_runs = np.zeros(sim_runs)
			
			# Placeholder to store all volatility values
			volatility_runs = np.zeros(sim_runs)
			
			# Placeholder to store all returns on investment
			return_on_investment_runs = np.zeros(sim_runs)
			
			# Placeholder to store all final portfolio values
			final_value_runs = np.zeros(sim_runs)
			max_sharpe_ratio = 0
			
			#!pip3 install progress progressbar2 alive-progress tqdm
			#import progressbar
			
			#sim_progress_bar = progressbar.ProgressBar(maxval=sim_runs).start()
			
			for i in range(sim_runs):
				# Generate random weights 
				weights = generate_portfolio_weights(n)
				# Store the weights
				weights_runs[i,:] = weights
				
				# Call "simulation_engine" function and store Sharpe ratio, return and volatility
				# Note that asset allocation is performed using the "asset_allocation" function  
				expected_portfolio_returns_runs[i], volatility_runs[i], sharpe_ratio_runs[i], final_value_runs[i], return_on_investment_runs[i] = simulation_engine(weights, initial_investment)
				#print("Simulation Run = {}".format(i))   
				#print("Weights = {}, Final Value = ${:.2f}, Sharpe Ratio = {:.2f}".format(weights_runs[i].round(3), final_value_runs[i], sharpe_ratio_runs[i]))   
				if sharpe_ratio_runs[i] > max_sharpe_ratio:
					max_sharpe_ratio = sharpe_ratio_runs[i]
					weights_max_sharpe = weights_runs[i]
					max_sharpe_expected_portfolio_returns_runs = expected_portfolio_returns_runs[i]
					max_sharpe_volatility_runs = volatility_runs[i]
				else:
					max_sharpe_ratio = max_sharpe_ratio
					weights_max_sharpe = weights_max_sharpe
					max_sharpe_expected_portfolio_returns_runs = max_sharpe_expected_portfolio_returns_runs
					max_sharpe_volatility_runs = max_sharpe_volatility_runs
				#print("Weights {} produces the min sharpe ratio of {} and has expected portfolio return of {} with a portfolio volatility of {}".format(weights_max_sharpe.round(3),max_sharpe_ratio,max_sharpe_expected_portfolio_returns_runs,max_sharpe_volatility_runs))
			
			#Identification of proposed optimal portfolio allocation for the selected portfolio of ETFs/Stocks, note the caveat that past performance is an imperfect indicator of future performance
			
			st.html("<h5>Optimal portfolio investment allocation given calibration parameters, selected tickers and initial investment ignoring risk appetite limitations.</h5>")
			st.write(':red[Note that past performance is an imperfect indication of future performance and this should not be considered to be financial advice but rather a useful tool contributing to the investment allocation decision.  Investors should consider implications of potential lack of diversification for positions representing 20%+ in single stocks (this would be less of a concern for broadly diversified ETF though).]')
			
			import numpy as np
			Asset_Allocation = np.around(weights_max_sharpe, decimals=2)*initial_investment
					
			list_of_investments = list(zip(etf_list, Asset_Allocation))
			list_of_investments_df = pd.DataFrame(list_of_investments, columns = ['Ticker', 'Investment_Amount'])
			
			import plotly.express as px
			col5, col6 = st.columns((1,1))
			with col5:
				st.dataframe(list_of_investments_df, hide_index=True)
				st.markdown('''
					[Get information on stock intrinsic value](https://www.alphaspread.com/)
				''')
			with col6:
				fig = px.pie(list_of_investments_df, values='Investment_Amount', names='Ticker')
				st.plotly_chart(fig, use_container_width=True)
			
			#Getting data from YFinance about a selected ticker
			import yfinance as yf
			selected_ticker_info = []
			selected_etf_info = []
			
			import math

			millnames = ['',' Thousand',' Million',' Billion',' Trillion']
			
			def millify(n):
				n = float(n)
				millidx = max(0,min(len(millnames)-1,
									int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
			
				return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
			
			for ticker in etf_list:
				result = yf.Ticker(ticker).info
				if result['quoteType'] != 'ETF':
					try:
						stock_items = [result['symbol'], result['longName'], result['sector'], result['currency'], result['currentPrice'], millify(result['marketCap']), result['trailingPE'], result['forwardPE']]
						selected_ticker_info.append(stock_items) 
					except:
						pass
				else:
					try:
						etf_items = [result['symbol'], result['longName'], result['currency'], result['previousClose'], result['fiftyTwoWeekLow'], result['fiftyTwoWeekHigh'], millify(result['totalAssets'])]
						selected_etf_info.append(etf_items) 
					except:
						pass
				
			if len(selected_ticker_info) > 0:
				selected_ticker_info_df = pd.DataFrame(selected_ticker_info, columns=['symbol', 'longName', 'sector', 'currency', 'currentPrice', 'marketCap', 'trailingPE', 'forwardPE'])
				ticker_df = pd.read_csv("Yahoo_Tickers.csv")
				selected_ticker_info_df = pd.merge(selected_ticker_info_df, ticker_df, left_on='symbol', right_on='Ticker', how='left', indicator=True)
				selected_ticker_info_df = selected_ticker_info_df.drop(columns=['Ticker', 'Name', '_merge'])
				selected_ticker_info_df.sort_values(by = 'forwardPE',  ascending=False, inplace = True)
				st.dataframe(selected_ticker_info_df, hide_index=True)
				st.write("In simple terms, a good P/E (Price divided by Earnings) ratio for an established company is lower than 20 (average across regions and industries is usually 20-25). When looking at the P/E ratio alone, the lower it is, the better.  It is however more meaningful to compare P/E Ratio for a stock to the average of the sector/industry from which it derives the majority of its income.  Also note that it is difficult to set guidelines for startups where future earnings are quite uncertain.")
			else:
				pass
			
			if len(selected_etf_info) > 0:
				selected_etf_info_df = pd.DataFrame(selected_etf_info, columns=['symbol', 'longName', 'currency', 'previousClose', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'totalAssets'])
				st.dataframe(selected_etf_info_df, hide_index=True)
				st.write("For ETFs with lower asset sizes (<AUD1bn) there may be liquidity issues (or larger discounts on selling particularly inadverse market conditions).")				
			else:
				pass
						
			#MARKOWITZ EFFICIENT FRONTIER
			
			st.html("<h5>Markowitz Efficient Frontier for the different portfolio weight combinations</h5>")
			
			# Create a DataFrame that contains volatility, return, and Sharpe ratio for all simualation runs
			sim_out_df = pd.DataFrame({'Volatility': volatility_runs.tolist(), 'Portfolio_Return': expected_portfolio_returns_runs.tolist(), 'Portfolio_Weights': weights_runs.round(2).tolist(), 'Sharpe_Ratio': sharpe_ratio_runs.tolist() })
			
			#In order for Portfolio_Weights to be included they need to be cast as a string rather than a series
			sim_out_df['Portfolio_Weights'] = sim_out_df['Portfolio_Weights'].astype(str)
			
			# Return Sharpe ratio, volatility corresponding to the best weights allocation (maximum Sharpe ratio)
			optimal_portfolio_return, optimal_volatility, optimal_sharpe_ratio, highest_final_value, optimal_return_on_investment = simulation_engine(weights_runs[sharpe_ratio_runs.argmax(), :], initial_investment)
			
			# Plot volatility vs. return for all simulation runs
			# Highlight the volatility and return that corresponds to the highest Sharpe ratio
			import plotly.graph_objects as go
			import matplotlib.pyplot as plt
			
			#!pip install seaborn
			import seaborn as sns
			
			import plotly.express as px
			try:
				fig = px.scatter(sim_out_df, x = 'Volatility', y = 'Portfolio_Return', size = 'Sharpe_Ratio', color = 'Portfolio_Weights')
				fig.add_trace(go.Scatter(x = [optimal_volatility], y = [optimal_portfolio_return], mode = 'markers', name = 'Optimal Point', marker = dict(size=[40], color = 'red')))
				fig.update_layout(coloraxis_colorbar = dict(y = 0.7, dtick = 5))
				fig.update_layout({'plot_bgcolor': "white"})
				fig.update_layout(showlegend=False)
				st.plotly_chart(fig)
				st.write(etf_list)
			except:
				st.write(":red[Could not produce Markowitz Frontier as returns for one or more assets are below the risk free rate.  Please remove these assets and rerun.]")
			
			##NOW WE CAPTURE THE RISK MANAGEMENT APPETITE SETTINGS
			
			st.html("<h5>Risk Appetite Inputs</h5>")
			
			Min_Port_Value = st.number_input("Minimum acceptable portfolio value by end of Investment Horizon", value=900000, step=50000)
			investor_risk_confidence = st.number_input("Percentage of the time that Portfolio value is required to exceed minimum acceptable value at end of investment horizon, 0.9 = 90%", value = 0.9, step = 0.01, min_value=0.5, max_value=0.99)
		
			##AND RUN CHECK ON RISK REPORTING
			
			#Using black76 model to identify whether the risk of the optimal portfolio is within required risk tolerance thresholds
			#!pip install scipy
			import scipy.stats as sct
			import math as math
			investor_risk_stddev = sct.norm.ppf(investor_risk_confidence)
			expected_optimal_portfolio_terminal_value = (initial_investment * ((1+max_sharpe_expected_portfolio_returns_runs)**investment_horizon)).round(2)
			min_terminal_value_at_tolerance = (expected_optimal_portfolio_terminal_value * math.exp(-1*investor_risk_stddev*max_sharpe_volatility_runs*math.sqrt(investment_horizon) - 0.5*max_sharpe_volatility_runs*investment_horizon)).round(2)
			if min_terminal_value_at_tolerance >= Min_Port_Value:
				st.write("The optimal portfolios minimum projected portfolio terminal value after {} years at your confidence level of {}% is \${:>,.0f} which is equal to or above your expressed minimum terminal value of \${:>,.0f}. The expected portfolio terminal value is \${:>,.0f}.".format(investment_horizon, investor_risk_confidence*100, min_terminal_value_at_tolerance, Min_Port_Value, expected_optimal_portfolio_terminal_value))
			elif min_terminal_value_at_tolerance < Min_Port_Value:
				st.write("The optimal portfolios minimum projected portfolio terminal value after {} years at your confidence level of {}% is \${:>,.0f} which is below your expressed minimum terminal value of \${:>,.0f}. The expected portfolio terminal value is \${:>,.0f}.".format(investment_horizon, investor_risk_confidence*100, min_terminal_value_at_tolerance, Min_Port_Value, expected_optimal_portfolio_terminal_value))
			
			sim_out_appetite_df = sim_out_df.copy()
			sim_out_appetite_df['Expected_Terminal_Value'] = (initial_investment * ((1+sim_out_appetite_df['Portfolio_Return'])**investment_horizon)).astype(float).round(2)
			for index, row in sim_out_appetite_df.iterrows():
				sim_out_appetite_df.at[index, 'Terminal_Value_at_Appetite'] = row['Expected_Terminal_Value'] * math.exp(-1*investor_risk_stddev*row['Volatility']*math.sqrt(investment_horizon) - 0.5*row['Volatility']*investment_horizon)
			sim_out_appetite_df['Terminal_Value_at_Appetite'] = sim_out_appetite_df['Terminal_Value_at_Appetite'].round(2)
			sim_out_within_appetite_df = sim_out_appetite_df[sim_out_appetite_df['Terminal_Value_at_Appetite'] >= Min_Port_Value]
			sim_out_within_appetite_df.sort_values(by = 'Sharpe_Ratio',  ascending=False, inplace = True)
			st.write(":blue[The following portfolios meet your risk appetite objectives from highest Sharpe Ratio (i.e. highest reward for risk) to lowest (top 5 displayed where available)]")
			sim_out_within_appetite_df.rename(columns={'Volatility':'Portfolio_Volatility'})
			st.dataframe(sim_out_within_appetite_df.head(5), hide_index=True)
			st.write(etf_list)
		except:
			pass
	else:
		st.write("Click the above button once selections final")

if selected == "Place Trades - Pick a Platform": 
	platform_html_code = """<h4 style='color: red;'>
	To save on costs, choose a platform that matches you investment style
	</h4>
	<p>
	Passive investors should choose a platform with no inactivity fees.  Active investors should choose a platform with low transaction fees and which gives them access to the assets they are looking to acquire. Some investors will look to avoid the operational risks which can arise from shares held in custody and not registered in their own name.
	</p>
	<p style='color: blue;'>
	Double click cells below to view all content.
	</p>"""
	st.markdown(platform_html_code, unsafe_allow_html=True)

	import pandas as pd
	platform_data = {'Platform': ['Interactive Brokers', 'eToro', 'Superhero', 'Tiger Brokers', 'CMC Markets', 'IG', 'Pearler', 'nabtrade', 'Selfwealth', 'ThinkMarkets'],
        'website': ['https://www.interactivebrokers.com.au','https://www.etoro.com','https://www.superhero.com.au','https://www.tiger.com','https://www.cmcmarkets.com','https://www.ig.com','https://pearler.com','https://www.nabtrade.com.au','https://www.selfwealth.com.au','https://www.thinkmarkets.com'],
        'Inactivity Fee': ['None','$10/month for inactivity over 12 months','None','None','$15/month for inactivity over 12 months','$50/quarter when less than 3 monthly trades','None','0.5% of portfolio value, triggered when you don’t make trades for 12 months','None','$30/month for inactivity over 12 months'],
        'Brokerage Fee': ['0.088% of trade value, for trades under A$3m','1% fee on crypto assets, 1.5% currency conversion fee, US$2 per side on stocks', '$5 flat fee on ASX stocks and ETFs, $0 on US stocks, 0.5% FX conversion fee', '0.055% or $5.5 minimum for ASX trades, 0.013 USD/share or $2 minimum for US trades', 'From $9.90 or 0.075% for ASX trades, from US$10 or 2c per share for US trades, 0.6% FX conversion fee', 'From $8 or 0.1% for ASX trades, from US$10 or 2c per share for US trades, 0.7% FX fee', 'From $9.50 per trade for ASX stocks and ETFs', 'From $14.95 or 0.11% for ASX trades, from US$14.95 or 0.11% for US trades, up to 0.6% FX fee', '$9.50 flat fee per trade for ASX stocks and ETFs, $9.50 flat fee per trade plus FX fee of 0.6% for US stocks and ETFs', 'From $8 or 0.08% for ASX trades, from US$9.95 or 2c per share for US trades, up to 1% FX fee'],
        'Tradeable Assets': ['Stocks, Crypto, CFDs, ETFs, options and futures','Stocks, ETFs, crypto assets', 'Stocks and ETFs', 'Stocks, ETFs, options and futures', 'Stocks, ETFs, CFDs and forex', 'Stocks, ETFs, CFDs and forex', 'Stocks and ETFs', 'Stocks and ETFs', 'Stocks and ETFs', 'Stocks, ETFs, CFDs and forex'],
        'Tradeable Indices': ['Wide range of markets','NYSE, NASDAQ, ASX, LSE, HKEX', 'ASX, NYSE and NASDAQ', 'ASX, NYSE, NASDAQ, HKEX and more', 'ASX, NYSE, NASDAQ and more', 'ASX, NYSE, NASDAQ and more', 'ASX', 'ASX, NYSE and NASDAQ', 'ASX, NYSE and NASDAQ', 'ASX, NYSE and NASDAQ'],
        'Registration Method': ['Custodial Ownership - Increased Risk','Custodial Ownership - Increased Risk', 'Custodial Ownership - Increased Risk', 'Registered in Investors Name - Lower Risk', 'Registered in Investors Name - Lower Risk', 'Custodial Ownership - Increased Risk', 'Registered in Investors Name - Lower Risk', 'Registered in Investors Name - Lower Risk', 'Registered in Investors Name - Lower Risk', 'Custodial Ownership - Increased Risk']}

	platform_data_df = pd.DataFrame(platform_data)
	
	st.dataframe(
    platform_data_df,
    column_config={
        "website": st.column_config.LinkColumn()
    }
	,hide_index = True)
