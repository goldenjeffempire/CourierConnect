
from django.conf import settings
from typing import List, Dict


class AIChatService:
    """
    AI-powered customer support chat service
    """
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY if hasattr(settings, 'OPENAI_API_KEY') else None
        self.system_prompt = """You are a helpful customer support agent for Courier Core, 
        a professional package delivery service. You can help with:
        - Tracking shipments
        - Pricing information
        - Delivery estimates
        - General inquiries
        - Account assistance
        
        Be professional, friendly, and concise. If you need specific tracking numbers or 
        account details, ask the customer to provide them."""
    
    def get_response(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """
        Get AI response for user message
        """
        if not self.api_key:
            return self._get_fallback_response(user_message)
        
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": user_message})
            
            # Note: This would use OpenAI API in production
            # For demo, return contextual response
            return self._get_contextual_response(user_message)
            
        except Exception as e:
            return self._get_fallback_response(user_message)
    
    def _get_contextual_response(self, message: str) -> str:
        """
        Provide contextual responses based on keywords
        """
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['track', 'tracking', 'where', 'status']):
            return "I can help you track your shipment! Please provide your tracking number (12 characters), and I'll look up the current status for you."
        
        elif any(word in message_lower for word in ['price', 'cost', 'quote', 'how much']):
            return "Our pricing is based on weight, distance, and service type. Standard delivery starts at $5 base fee plus $0.50 per pound and $0.10 per mile. Express delivery is 1.5x standard rates. Would you like to get a detailed quote?"
        
        elif any(word in message_lower for word in ['delivery', 'how long', 'when', 'estimate']):
            return "Delivery times vary by service: Standard delivery takes 3-5 business days, while Express delivery takes 1-2 business days. Do you have a specific shipment you'd like me to check?"
        
        elif any(word in message_lower for word in ['create', 'ship', 'send', 'new']):
            return "To create a new shipment, click on 'Create Shipment' in the navigation menu or your dashboard. You'll need pickup and delivery addresses, package details, and payment information. Can I help you with anything specific about the shipping process?"
        
        elif any(word in message_lower for word in ['payment', 'pay', 'credit card']):
            return "We accept all major credit cards through our secure Stripe payment system. Payment is processed after you create your shipment and before we assign it to a courier. Is there a specific payment question I can help with?"
        
        elif any(word in message_lower for word in ['cancel', 'refund']):
            return "You can cancel a shipment before it's picked up by the courier. Refunds are processed within 5-7 business days. Would you like me to help you cancel a specific shipment?"
        
        elif any(word in message_lower for word in ['help', 'support', 'assistance']):
            return "I'm here to help! I can assist with tracking shipments, pricing information, delivery estimates, and general questions about our service. What would you like to know?"
        
        else:
            return "Thank you for contacting Courier Core! I'm here to help with tracking, pricing, deliveries, and any questions about our service. How can I assist you today?"
    
    def _get_fallback_response(self, message: str) -> str:
        """
        Fallback response when AI is not available
        """
        return "Thank you for your message. Our support team will assist you shortly. For immediate help, please visit our FAQ section or call our 24/7 hotline."
