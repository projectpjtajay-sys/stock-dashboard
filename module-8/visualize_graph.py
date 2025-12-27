#!/usr/bin/env python3
"""
LangGraph Multi-Agent System Visualization Demo

This script demonstrates how to visualize the multi-agent system graph
using LangGraph's built-in visualization capabilities.

Usage:
    python visualize_graph.py [--format ascii|mermaid|png|all]
"""

import argparse
import sys
import os

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents import MultiAgentSystem

def main():
    parser = argparse.ArgumentParser(description="Visualize Multi-Agent System Graph")
    parser.add_argument(
        '--format', 
        choices=['ascii', 'mermaid', 'png', 'all'], 
        default='all',
        help='Visualization format (default: all)'
    )
    
    args = parser.parse_args()
    
    print("🤖 Multi-Agent System Graph Visualization")
    print("=" * 60)
    
    # Initialize the multi-agent system
    try:
        print("Initializing Multi-Agent System...")
        multi_agent = MultiAgentSystem()
        print("✅ Multi-Agent System initialized successfully!\n")
    except Exception as e:
        print(f"❌ Error initializing Multi-Agent System: {e}")
        return
    
    # Generate visualizations based on format selection
    if args.format in ['ascii', 'all']:
        print("📝 ASCII Visualization:")
        print("-" * 30)
        try:
            multi_agent.visualize_graph_ascii()
        except Exception as e:
            print(f"❌ ASCII visualization failed: {e}")
        print("\n")
    
    if args.format in ['mermaid', 'all']:
        print("🧜‍♀️ Mermaid Diagram:")
        print("-" * 30)
        try:
            mermaid_output = multi_agent.visualize_graph_mermaid()
            if mermaid_output:
                print("✅ Mermaid diagram generated successfully!")
                print("💡 You can copy the Mermaid code and paste it into https://mermaid.live/ to view the diagram")
        except Exception as e:
            print(f"❌ Mermaid visualization failed: {e}")
        print("\n")
    
    if args.format in ['png', 'all']:
        print("🖼️  PNG Image:")
        print("-" * 30)
        try:
            multi_agent.visualize_graph_png("multiagent_graph_demo.png")
            print("✅ PNG visualization generated successfully!")
        except Exception as e:
            print(f"❌ PNG visualization failed: {e}")
            print("💡 Install graphviz for PNG support: pip install graphviz")
        print("\n")
    
    print("🎉 Visualization complete!")
    print("\n📚 Available API Endpoints for Web Visualization:")
    print("   • GET /api/graph/ascii   - ASCII representation")
    print("   • GET /api/graph/mermaid - Mermaid diagram code")
    print("   • GET /api/graph/png     - PNG image download")

if __name__ == "__main__":
    main() 