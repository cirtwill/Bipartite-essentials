############################################################
###		Ensure plants are columns, extract column names 			###
############################################################

# Double-checked taxonomies from the MSc students are in final_taxonomy.csv and inputs_to_outputs.tsv, both in data/plant_phylogeny
# Produce phylomatic tree
data/plant_phylogeny/output : data/plant_phylogeny/final_taxonomy.tsv 
	cd data/plant_phylogeny && \
	cp final_taxonomy.tsv phylo && \
	

# Check that plants are columns in all matrices
data/Uncorrected_Matrices/Stouffer_Ecology_Matrices/%.csv.flipped : code/refine_matrices/ensure_plants_columns.py data/Uncorrected_Matrices/Stouffer_Ecology_Matrices/*.csv data/Uncorrected_Matrices/Plant_herbivore_matrices/*.csv
	cd code/refine_matrices && \
	python ensure_plants_columns.py && \
	echo 'orientation checked' && \
	cd ../../



# Get original plant names
data/plant_phylogeny/original_names.tsv : code/refine_matrices/plant_name_extractor.py data/Uncorrected_Matrices/Stouffer_Ecology_Matrices/*.csv data/Uncorrected_Matrices/Plant_herbivore_matrices/*.csv
	cd code/refine_matrices && \
	python plant_name_extractor.py && \
	echo $@ && \
	cd ../../

## Lovely masters students checked the names.
## They produced the files final_taxonomy.tsv (slash-delimited phylomatic input)
## and inputs_to_outputs.tsv (tab-delimited in-name to out-name)
# # Correct plant names - this step may not auto-run well.
# data/plant_phylogeny/corrected_names.tsv : code/refine_matrices/auto_taxize.R data/plant_phylogeny/original_names.tsv
# 	cd code/refine_matrices && \
# 	echo 'beginning taxize' && \
# 	Rscript auto_taxize.R && \
# 	echo 'taxize has succeeded' && \
# 	echo $@ && \
# 	cd ../../


# # DO NOT RUN create_corrected_matrices until taxize complete.

# I would like to split the final taxonomy into PH and PP lists for phylomatic purposes while I correct the matrices
data/Corrected_Matrices/%/%.csv data/plant_phylogeny/poll_tree.tsv data/plant_phylogeny/herb_tree.tsv : data/plant_phylogeny/corrected_names.tsv data/Uncorrected_Matrices/Plant_herbivore_matrices/*.csv data/Uncorrected_Matrices/Stouffer_Ecology_Matrices/*.csv code/refine_matrices/create_corrected_matrices.py
	cd code/refine_matrices && \
	python create_corrected_matrices.py && \
	echo 'phy datafile made' && \
	echo $@ && \
	cd ../../


### Now create a phylogeny for each web using phylomatic (Zanne 2014 tree) and the phylogeny lists in data/plant_phylogeny/PP_webs and data/plant_phylogeny/PH_webs
### Correct the couple of webs with missing nodes using commented-out code in create_corrected_matrices.py

# Calculate distances and overlaps between plant pairs using Jaccard dissimilarity to calculate overlap
# Note: calculates observed overlaps, not randomized ones.
data/Jaccard/Overlap_dist/%/%.csv data/Jaccard/families_to_networks/families_by_network.csv : data/plant_phylogeny/trees/*.new data/Corrected_Matrices/*/*_corrected.csv
	cd code/ && \
	Rscript Jaccard_overlap_vs_distance.R && \
	echo 'Distance and overlap datafile made' && \
	cd ../

# The following steps are quite slow and may require working in chunks to not fill up the hard drive.
# Make the randomized and randomized-randomized versions of each matrix
data/Random_matrices/%_rand.csv : data/Corrected_Matrices/*/* code/Mantel_randomiser.R
	cd code/ && \
	Rscript Mantel_randomiser.R && \
	echo 'Many randomized matrices made' && \
	cd ../

# Calculate overlaps in random matrices and then delete them if space is a concern.
data/Jaccard/Random_Matrices/%.csv : data/Random_Matrices/*/* data/Random_Random_Matrices/*/*/* code/Random_Jaccard_overlap_vs_distance.R
	cd code/ && \
	Rscript Random_Jaccard_overlap_vs_distance.R && \
	echo 'random overlaps calculated' && \
	cd ../

# code/outfile_checker.R and code/randomisation_counter.py are helpful little things to track progress of overlap calculations

# Perform regressions of overlap vs. distance for random and doube-random matrices
data/Jaccard/Random_Regressions/%.tsv : data/Jaccard/Random_Matrices/*/*.csv data/Jaccard/Overlap_dist/*/*.csv code/Jaccard_random_regressions.R
	cd code/ && \
	Rscript Jaccard_random_regressions.R && \
	echo 'slopes for random matrices calculated' && \
	cd ../

# No longer relies on random regressions - observed and random data will be collected later
data/Jaccard/Observed_Regression/observed_coefficients.tsv : data/Jaccard/Overlap_dist/*/*.csv code/Jaccard_regressions.R
	cd code/ && \
	Rscript Jaccard_regressions.R && \
	echo 'observed slopes calculated' && \
	cd ../


# The Jaccard regressions requires random matrices so can't run yet.
data/Jaccard/Observed_Regression/observed_vs_random.tsv : data/Jaccard/Random_Regressions/*.tsv  data/Jaccard/Observed_Regression/observed_coefficients.tsv code/collate_randoms.R
	cd code/ && \
	Rscript collate_randoms.R && \
	echo 'observed and random slopes collected per network' && \
	cd ../

# Testing whether slopes are related to community composition, observed only
data/Jaccard/families_to_networks/permanova_table.tsv : data/Jaccard/Observed_Regression/observed_coefficients.tsv data/Jaccard/families_to_networks/families_by_network.csv code/families_to_networks.R
	cd code/ &&\
	Rscript families_to_networks.R && \
	echo 'slopes vs community composition tested' && \
	cd ../

data/

# Now then... on to plots I guess. 


5) Make plots of p-values for randomisations of randomisations of each network (many plots? 10 nets/plot?)


# 6) Do observed and random for within-family stuff ?



all : manuscript/Figures/dataplots/degree_*.eps  
#$^ is for "all the prerequisites of this file"
#$......
# $@ is short for "the target of this rule"

# Test the signals for degree, partners, and spit out the appropriate figures
manuscript/Figures/dataplots/degree_%.eps : code/create_figures/signal_barplots.py data/bynetwork_signal_*.csv data/bynetwork_signal_degree.csv
	echo 'Making degree barplots' && \
	cd code/create_figures && \
	python signal_barplots.py && \
	cd ../../

data/bynetwork_signal_partners.csv : code/signal_test_partners.R data/plant_phylogeny/dated_tree.new data/plant_phylogeny/corrected_names.tsv data/Corrected_Matrices/*/*.csv
	cd code && \
	echo 'Running tests on partners' && \
	Rscript signal_test_partners.R && \
	cd  ../

data/bynetwork_signal_degree.csv : code/signal_test_degree.R data/plant_phylogeny/dated_tree.new data/plant_phylogeny/corrected_names.tsv data/Corrected_Matrices/*/*.csv
	cd code && \
	echo 'Running tests on degree' && \
	Rscript signal_test_degree.R && \
	cd  ../
# Checked down to here.

# Correct plant names - this step may not auto-run well.
data/plant_phylogeny/corrected_names.tsv : code/refine_matrices/auto_taxize.R data/plant_phylogeny/original_names.tsv
	cd code/refine_matrices && \
	echo 'beginning taxize' && \
	Rscript auto_taxize.R && \
	echo 'taxize has succeeded' && \
	echo $@ && \
	cd ../../





# ## Test the strength of signal in degree and partners (might as well do both at once?)
# data/bynetwork_signal_%.csv : code/signal_test_degree.R code/signal_test_partners.R code/Test.Kmult.R data/Corrected_Matrices/Plant_herbivore_matrices/*.csv data/Corrected_Matrices/Stouffer_Ecology_Matrices/*.csv data/plant_phylogeny/dated_tree.new data/plant_phylogeny/corrected_names.tsv
# 	cd code/ && \
# 	Rscript signal_test_degree.R && \
# 	Rscript signal_test_partners.R && \
# 	cd ../


# ## Calculate overlap and distance for all pairs (slowest step) - does the motiflike distance
# data/Overlap_dist/%_dist.csv : code/overlap_vs_distance.R data/plant_phylogeny/dated_tree.new data/Corrected_Matrices/Plant_herbivore_matrices/*.csv data/Corrected_Matrices/Stouffer_Ecology_Matrices/*.csv
# 	cd code/ && \
# 	Rscript overlap_vs_distance.R && \
# 	cd ../


# ## Produce the regression summary tables
# data/Regressions/%_%.tsv : code/overlap_regressions.R data/Overlap_dist/Plant_herbivore_matrices/*.csv data/Overlap_dist/Stouffer_Ecology_Matrices/*.csv
# 	cd code/ && \
# 	Rscript overlap_regressions.R && \
# 	cd ../


# ## To make figures:
# manuscript/Figures/dataplots/Family/allfams_%.eps : code/create_figures/cladewise_plots.py data/Regressions/Family/*_*_reg_fixef.tsv data/Regressions/Family/*_*_reg_ranef.tsv data/Regressions/Family/overall_*_reg_*.tsv
# 	cd code/create_figures && \
# 	python cladewise_plots.py && \
# 	cd ../../

# # Same file makes talk regression figures, regression figures with ranked distances
# manuscript/Figures/dataplots/scaled_regression_lines_full.eps : code/create_figures/regression_line_plot.py data/Regressions/*_reg_fixef.tsv data/Regressions/*_reg_ranef.tsv data/Regressions/*_reg_unranked_scaled_fixef.tsv data/Regressions/*_reg_unranked_scaled_ranef.tsv
# 	cd code/create_figures && \
# 	python regression_line_plot.py && \
# 	cd ../../


# Same file makes degree one, pp, partners full, one, pp, and scatterplot.
manuscript/Figures/dataplots/degree_full.eps : code/create_figures/signal_barplots.py data/bynetwork_signal_*.csv
	cd code/create_figures && \
	python signal_barplots.py && \
	cd ../../



