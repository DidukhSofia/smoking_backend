from backend.app.models import User
user = User.objects.create_user(email='user@example.com', password='password', startAmountOfCigarettes=10, priceOfPack=5, amountCigarettesInPack=20, progressDays=30)
print(user.calculate_saved_cigarettes())
print(user.calculate_saved_money())
