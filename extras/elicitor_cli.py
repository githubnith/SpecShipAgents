from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart, UserPromptPart
from rich.console import Console, ConsoleOptions, RenderResult
from pydantic import ValidationError
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.live import Live
from rich.text import Text
from pydantic_ai import Agent
from dotenv import load_dotenv
from typing import List
import asyncio
import logfire
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.elicitor_agent import elicitor_agent

# Load environment variables
load_dotenv()

# Configure logfire to suppress warnings
logfire.configure(send_to_logfire='never')

class CLI:
    def __init__(self):
        self.messages: List[ModelMessage] = []
        self.console = Console()

    async def chat(self):
        print("Requirements Elicitor CLI (type 'quit' to exit)")
        print("Please provide your business requirements. I will guide you through the process.")
        print("\nEnter your message:")
        
        while True:
            user_input = input("> ").strip()
            if user_input.lower() == 'quit':
                break

            # Run the agent with streaming
            requirement_details = None
            with Live('', console=self.console, vertical_overflow='visible') as live:
                async with elicitor_agent.run_stream(user_input, message_history=self.messages) as result:
                    async for message, last in result.stream_structured(debounce_by=0.1):  
                        try:
                            current_details = await result.validate_structured_result(  
                                message,
                                allow_partial=True  # Always allow partial results
                            )
                            if current_details and current_details.response:
                                requirement_details = current_details
                                live.update(Markdown(requirement_details.response))
                        except ValidationError as e:
                            if last:  # Only log validation errors on the last message
                                print(f"\nValidation error: {e}")
                            continue
                        except Exception as e:
                            if last:
                                print(f"\nError processing response: {e}")
                            continue
                    
                    if not requirement_details or not requirement_details.response:
                        print("\nNo valid response received from the agent. Please try again.")
                        return

            # Store the user message
            self.messages.append(
                ModelRequest(parts=[UserPromptPart(content=user_input)])
            )

            # Add the final response from the agent
            self.messages.append(
                ModelResponse(parts=[TextPart(content=requirement_details.response)])
            )

            # If all details are gathered, show a summary
            if requirement_details.all_details_given:
                self.console.print("\n[green]✓ All required information has been gathered![/green]")
                self.console.print("\n[bold]Requirement Summary:[/bold]")
                self.console.print(f"• Specific Requirement: {requirement_details.specific_requirement}")
                self.console.print(f"• LoB Design Approval: {requirement_details.lob_design_approval}")
                self.console.print(f"• LoB Senior Approval: {requirement_details.lob_senior_approval}")
                if requirement_details.test_cases:
                    self.console.print("\n[bold]Test Cases:[/bold]")
                    for test_case in requirement_details.test_cases:
                        self.console.print(f"  • {test_case}")
                if hasattr(requirement_details, 'development_details'):
                    self.console.print("\n[bold]Development Details:[/bold]")
                    dev = requirement_details.development_details
                    self.console.print(f"  • New Build: {'Yes' if dev.is_new_build else 'No'}")
                    self.console.print(f"  • BE Build Required: {'Yes' if dev.requires_be_build else 'No'}")
                    self.console.print(f"  • Mobile Required: {'Yes' if dev.requires_mobile else 'No'}")
                    self.console.print(f"  • Shared Services: {'Yes' if dev.requires_shared_services else 'No'}")
                self.console.print(f"\n• Business Value: {requirement_details.business_value}")
                self.console.print(f"• Success Definition: {requirement_details.success_definition}")
                self.console.print("\n[bold]Success Metrics:[/bold]")
                for metric in requirement_details.success_metrics:
                    self.console.print(f"  • {metric}")
                self.console.print(f"\n• Target Date: {requirement_details.target_date}")
                self.console.print(f"• Date Implications: {requirement_details.date_implications}")
                if requirement_details.impacted_applications:
                    self.console.print("\n[bold]Impacted Applications:[/bold]")
                    for app in requirement_details.impacted_applications:
                        self.console.print(f"  • {app}")

async def main():
    cli = CLI()
    await cli.chat()

if __name__ == "__main__":
    asyncio.run(main())
