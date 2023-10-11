class LabelHelper:
    @staticmethod
    def snake_case_to_label(snake_case_label: str) -> str:
        return snake_case_label.replace("_", " ").capitalize()
