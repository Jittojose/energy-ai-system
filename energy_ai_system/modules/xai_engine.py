class XAIEngine:
    def __init__(self, model):
        self.model = model

    def get_feature_importance(self, feature_names):
        importances = self.model.feature_importances_

        importance_dict = {}
        for feature, importance in zip(feature_names, importances):
            importance_dict[feature] = round(importance * 100, 2)

        return importance_dict

    def get_top_feature(self, importance_dict):
        top_feature = max(importance_dict, key=importance_dict.get)
        return top_feature