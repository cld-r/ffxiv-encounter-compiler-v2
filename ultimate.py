from abc import ABC, abstractmethod

class Ultimate(ABC):
    @abstractmethod
    def get_short_name(self):
        pass

    @abstractmethod
    def get_long_name(self):
        pass

    @abstractmethod
    def get_ability_names(self):
        pass

    def get_priority_list(self):
        return list(reversed(self.get_ability_names().keys()))

    def get_filter_expression(self):
        abilities = "', '".join(self.get_ability_names().keys())
        return f"ability.name IN ('{abilities}')" 

class FRU(Ultimate):
    def get_short_name(self):
        return "FRU"
    
    def get_long_name(self):
        return "Futures Rewritten (Ultimate)"

    def get_ability_names(self):
        return {
            'Utopian Sky': 'Utopian',
            'Fall of Faith': 'Faith',
            'Diamond Dust': 'DD',
            'Mirror, Mirror': 'Mirror',
            'Light Rampant': 'LR',
            'Endless Ice Age': 'Intermission',
            'Ultimate Relativity': 'UR',
            'Apocalypse': 'Apoc',
            'Darklit Dragonsong': 'Darklit',
            'Crystallize Time': 'CT',
            'Fulgent Blade': 'Pandora',
            'Paradise Lost': 'Enrage'
        }