from abc import ABC, abstractmethod

class Expr(ABC):

    @abstractmethod
    def eval(self, ctx):
        pass

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def get_type(self):
        pass

class Statements(ABC):

    @abstractmethod
    def eval(self, ctx):
        pass

class Statement(ABC):

    @abstractmethod
    def eval(self, ctx):
        pass

class Assign(ABC):

    @abstractmethod
    def eval(self, ctx):
        pass
    
    #return the variable name (in the internal representation) that is being assigned to
    @abstractmethod
    def get_ref(self):
        pass

    @abstractmethod
    def get_value(self):
        pass

class RefExpr(ABC):

    @abstractmethod
    def eval(self, ctx):
        pass

    @abstractmethod
    def set_value(self, ctx):
        pass

class FunctionCall(ABC):

    @abstractmethod
    def eval(self, ctx):
        pass

class IfStatement(ABC):

    @abstractmethod
    def eval(self, ctx):
        pass

class ReturnVars(ABC):

    @abstractmethod
    def eval(self, ctx):
        pass

class ArrayVals(ABC):

    @abstractmethod
    def eval(self, ctx):
        pass

class MatrixRowInner(ABC):

    @abstractmethod
    def eval(self, ctx):
        pass

class Args(ABC):

    @abstractmethod
    def eval(self, ctx):
        pass
    
    @abstractmethod
    def get_values(self):
        pass


