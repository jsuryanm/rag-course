from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel,Field
from typing import Literal
from enum import Enum 

from .calculator import Calculator

class OperationType(str,Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"

class CalculationRequest(BaseModel):
    """This is an input contract.
    Request Model for calculation endpoint.
    Client sends us JSON like:
    {
        "operation": "add",
         num1: float,
         num2: float
    }
    Validates incoming calculation requests with Pydantic"""
    
    operation: OperationType = Field(...,description="The mathematical operation to perform")
    num1: float = Field(...,description="First operand")
    num2: float = Field(...,description="Second operand")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "operation": "add",
                    "num1": 10,
                    "num2": 5,
                    "result": 15
                }
            ]
        }
    }

class CalculationResponse(BaseModel):
    """
    This is the output contract.
    Response model for calculation endpoint.

    Provides structured response with operation details and result.
    FastAPI will respond in this format for every successful response
    """
    operation: str = Field(..., description="The operation that was performed")
    num1: float = Field(..., description="First operand")
    num2: float = Field(..., description="Second operand")
    result: float = Field(..., description="The calculated result")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "operation": "add",
                    "num1": 10,
                    "num2": 5,
                    "result": 15
                }
            ]
        }
    }


calculator = Calculator()

app = FastAPI(title="Calculator API",
              description="Modular calculator api",
              version="1.0.0",
              docs_url="/docs",
              redoc_url="/redoc")


@app.get("/",tags=["General"])
def root():
    """Welcome endpoint with API information"""

    return {"message":"Welcome to Calculator API - version 2",
            "description":"A modular calculator with OOP based business logic",
            "version":"1.0.0",
            "architecture":"OOP with seperated modules",
            
            "features": [
            "Object-oriented design",
            "Separated business logic",
            "Testable components",
            "Pydantic validation"],
            
            "endpoints": {
            "documentation": "/docs",
            "calculate": "POST /calculate",
            "operations": "GET /operations"}
        }

@app.get("/operations",tags=["General"])
def get_operations():
    """
    Get list of all supported operations.

    This endpoint dynamically fetches supported operations from the Calculator class.
    """
    supported_ops = calculator.get_supported_operations()

    operations_info = []

    for op in supported_ops:
        if op == "add":
            info = {"operation":op,"description":"Addition (a + b)","symbol": "+"}

        elif op == "subtract":
            info = {"operation": op, "description": "Subtraction (a - b)", "symbol": "-"}
        elif op == "multiply":
            info = {"operation": op, "description": "Multiplication (a × b)", "symbol": "×"}
        elif op == "divide":
            info = {"operation": op, "description": "Division (a ÷ b)", "symbol": "÷"}
        else:
            info = {"operation": op, "description": f"Operation: {op}", "symbol": "?"}
        
        operations_info.append(info)
    
    return {"supported_operations":operations_info,
            "total_count":len(operations_info)}

@app.post('/calculate',
          response_model=CalculationResponse,
          status_code=status.HTTP_200_OK,
          tags=["Calculator"])

def calculate(request: CalculationRequest):
    """
    Perform a calculation using the Calculator class.

    This endpoint delegates all business logic to the Calculator class,
    maintaining clean separation of concerns between API and business logic layers.

    Supports the following operations:
    - **add**: Addition (num1 + num2)
    - **subtract**: Subtraction (num1 - num2)
    - **multiply**: Multiplication (num1 × num2)
    - **divide**: Division (num1 ÷ num2)

    Args:
        request: CalculationRequest with operation and operands

    Returns:
        CalculationResponse with the result

    Raises:
        HTTPException 400: If division by zero is attempted or invalid operation
        HTTPException 422: If invalid parameters (handled by Pydantic)
    """
    try:
        result = calculator.calculate(operation=request.operation.value,
                                      num1=request.num1,
                                      num2=request.num2)
        
        return CalculationResponse(operation=request.operation.value,
                                   num1=request.num1,
                                   num2=request.num2,
                                   result=result)
    
    except ZeroDivisionError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An unexpected error: {str(e)}")

@app.get("/health", tags=["General"])
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {
        "status": "healthy",
        "calculator_ready": calculator is not None,
        "version": "2.0.0"
    }