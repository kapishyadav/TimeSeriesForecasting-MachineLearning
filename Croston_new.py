import numpy as np
import pandas as pd

class Croston_new:
	def Croston(total_data):
		extra_periods=12
		alpha=0.4
		d = np.array(total_data) 
		cols = len(d) 
		# Historical period length
		d = np.append(d,[np.nan]*extra_periods) # Append np.nan into the demand array to cover future periods
		
		#level (a), periodicity(p) and forecast (f)
		a,p,f = np.full((3,cols+extra_periods),np.nan)
		q = 1 #periods since last demand observation
		
		# Initialization
		first_occurence = np.argmax(d[:cols]>0)
		a[0] = d[first_occurence]
		p[0] = 1 + first_occurence
		f[0] = a[0]/p[0]
		# Create all the t+1 forecasts
		for t in range(0,cols):        
			if d[t] > 0:
				a[t+1] = alpha*d[t] + (1-alpha)*a[t] 
				p[t+1] = alpha*q + (1-alpha)*p[t]
				f[t+1] = a[t+1]/p[t+1]
				q = 1           
			else:
				a[t+1] = a[t]
				p[t+1] = p[t]
				f[t+1] = f[t]
				q += 1
		   
		# Future Forecast 
		a[cols+1:cols+extra_periods] = a[cols]
		p[cols+1:cols+extra_periods] = p[cols]
		f[cols+1:cols+extra_periods] = f[cols]
						  
		df = pd.DataFrame.from_dict({"Demand":d,"Forecast":f,"Period":p,"Level":a,"Error":d-f})
		return df["Forecast"].iloc[-1]


	def Croston_calculate(total_data, no_of_months):
		predictions=[]
		for i in range(0,no_of_months):
			yhat = Croston(total_data)
			total_data.append(yhat)
			predictions.append(yhat)
		return predictions


# total_data = [682,345,514,379,470,500,625,245,457,354,258,554,585,419,280,352,431,
# 			298,370,506,465,236,708,480,513,715,206,136,293,395,217,397,573,421,326,357,
# 			398,595,367,487,184,409,348,443,299,451,301,399,460,373,285,396,419,182,306,472,429,277,154,397,296]

# print(Croston_calculate(total_data,24))
# #print(Croston(total_data))