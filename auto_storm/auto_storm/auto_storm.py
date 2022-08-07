# A collection of functions


def bmi(mass, height):
	bmi_formula = mass//height**2

	if bmi_formula < 18.5: 
		print('Body mass index is ==> ', bmi_formula)
		print('under')

	elif bmi_formula > 23:
		print('Body mass index is ==> ', bmi_formula)
		print('over')

	elif bmi_formula > 30:
		print('Body mass index is ==> ', bmi_formula)
		print('obese')

	return bmi_formula