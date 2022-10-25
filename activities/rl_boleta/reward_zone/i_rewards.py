from abc import ABC, abstractmethod

class IRewards(ABC):
    
    @abstractmethod
    def calculate_reward(agente) -> int:
        pass
    
