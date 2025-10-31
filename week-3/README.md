# Week-3
In week-3 we compare jailbreak effectiveness across multiple models and visualize overall performance trends using aggregated data.  
For week 3 we combined results of TinyLlama, DistilGPT-2, and Falcon RW-1B into a unified Markdown table.

Week 3 focused on comparing jailbreak effectiveness across the three selected models—TinyLlama 1.1B-Chat, DistilGPT-2, and Falcon RW-1B—to understand how different model architectures and tuning levels respond to the same set of attack techniques. The results from Week 2 were consolidated into a unified dataset, and each model’s responses were scored numerically to allow direct comparison. Visualization using Matplotlib was introduced to represent effectiveness scores through bar charts and comparative graphs, providing a clear picture of the behavioral differences among the models.

The analysis showed that Falcon RW-1B exhibited the highest responsiveness to persona-based and emotional jailbreak prompts, indicating greater susceptibility in instruction-aligned models. TinyLlama 1.1B displayed moderate vulnerability, occasionally following manipulative instructions but maintaining partial restraint in certain cases. DistilGPT-2, which is not instruction-tuned, remained largely unaffected and mostly echoed prompts without meaningful deviation. These comparisons demonstrated a strong correlation between model alignment and jailbreak sensitivity. Overall, Week 3 established a visual and analytical baseline for model behavior, laying the groundwork for the deeper evaluation and statistical analysis performed in Week 4.

