"""
Generate OpenAPI schema for Astrologer API
Open-source version - no RapidAPI dependencies
"""

from app.main import app
import json


def dump_schema(output_file_path):
    """
    Generates a clean OpenAPI schema without proprietary dependencies
    """
    openapi_data = app.openapi()

    # Set the base URL to localhost for development
    # Users can change this in production to their own domain
    openapi_data['servers'] = [
        {
            "url": "http://localhost:8000",
            "description": "Local development server"
        },
        {
            "url": "https://your-domain.vercel.app",
            "description": "Production server (update with your domain)"
        }
    ]

    # Save the clean OpenAPI JSON file
    with open(output_file_path, 'w') as file:
        json.dump(openapi_data, file, indent=2)

    print(f"✅ OpenAPI schema generated successfully at: {output_file_path}")
    print("📝 You can validate it at: https://editor-next.swagger.io/")
    print("🚀 100% Open-Source - No proprietary dependencies!")


if __name__ == "__main__":
    dump_schema("openapi.json")
