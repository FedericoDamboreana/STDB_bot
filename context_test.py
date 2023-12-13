from managers.context_manager import ContextManager

manager = ContextManager('./store')
manager.load_db()
context = manager.get_optimized_context("How do I access Infographics inside Business Analyst?")
print("=====================================================================")
print("\nCONTEXT\n")
print(context)
