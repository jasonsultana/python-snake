class Utils:    
    # Eg: 
    # 5 x (12/5) [2.4]->2 = 10
    # 50 x (82/50) [1.64]->2 = 100
    @staticmethod
    def round_to(x, base = 5):
        return base * round(x / base)