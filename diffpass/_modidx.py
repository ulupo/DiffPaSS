# Autogenerated by nbdev

d = { 'settings': { 'branch': 'main',
                'doc_baseurl': '/DiffPASS',
                'doc_host': 'https://Bitbol-Lab.github.io',
                'git_url': 'https://github.com/Bitbol-Lab/DiffPASS',
                'lib_path': 'diffpass'},
  'syms': { 'diffpass.base': { 'diffpass.base.DiffPASSMixin': ('base.html#diffpassmixin', 'diffpass/base.py'),
                               'diffpass.base.DiffPASSMixin.reduce_num_tokens': ( 'base.html#diffpassmixin.reduce_num_tokens',
                                                                                  'diffpass/base.py'),
                               'diffpass.base.DiffPASSMixin.validate_information_measure': ( 'base.html#diffpassmixin.validate_information_measure',
                                                                                             'diffpass/base.py'),
                               'diffpass.base.DiffPASSMixin.validate_inputs': ( 'base.html#diffpassmixin.validate_inputs',
                                                                                'diffpass/base.py'),
                               'diffpass.base.DiffPASSMixin.validate_permutation_cfg': ( 'base.html#diffpassmixin.validate_permutation_cfg',
                                                                                         'diffpass/base.py'),
                               'diffpass.base.DiffPASSMixin.validate_reciprocal_best_hits_cfg': ( 'base.html#diffpassmixin.validate_reciprocal_best_hits_cfg',
                                                                                                  'diffpass/base.py'),
                               'diffpass.base.DiffPASSMixin.validate_similarities_cfg': ( 'base.html#diffpassmixin.validate_similarities_cfg',
                                                                                          'diffpass/base.py'),
                               'diffpass.base.DiffPASSMixin.validate_similarity_kind': ( 'base.html#diffpassmixin.validate_similarity_kind',
                                                                                         'diffpass/base.py'),
                               'diffpass.base.EnsembleMixin': ('base.html#ensemblemixin', 'diffpass/base.py'),
                               'diffpass.base.EnsembleMixin._reshape_ensemble_param': ( 'base.html#ensemblemixin._reshape_ensemble_param',
                                                                                        'diffpass/base.py'),
                               'diffpass.base.EnsembleMixin._validate_ensemble_param': ( 'base.html#ensemblemixin._validate_ensemble_param',
                                                                                         'diffpass/base.py'),
                               'diffpass.base.scalar_or_1d_tensor': ('base.html#scalar_or_1d_tensor', 'diffpass/base.py')},
            'diffpass.constants': { 'diffpass.constants.SubstitutionMatrix': ('constants.html#substitutionmatrix', 'diffpass/constants.py'),
                                    'diffpass.constants.TokenizedSubstitutionMatrix': ( 'constants.html#tokenizedsubstitutionmatrix',
                                                                                        'diffpass/constants.py'),
                                    'diffpass.constants.get_blosum62_data': ('constants.html#get_blosum62_data', 'diffpass/constants.py')},
            'diffpass.data_utils': { 'diffpass.data_utils.dataset_tokenizer': ( 'data_utils.html#dataset_tokenizer',
                                                                                'diffpass/data_utils.py'),
                                     'diffpass.data_utils.generate_dataset': ('data_utils.html#generate_dataset', 'diffpass/data_utils.py'),
                                     'diffpass.data_utils.msa_tokenizer': ('data_utils.html#msa_tokenizer', 'diffpass/data_utils.py')},
            'diffpass.entropy_ops': { 'diffpass.entropy_ops.pointwise_shannon': ( 'entropy_ops.html#pointwise_shannon',
                                                                                  'diffpass/entropy_ops.py'),
                                      'diffpass.entropy_ops.smooth_mean_one_body_entropy': ( 'entropy_ops.html#smooth_mean_one_body_entropy',
                                                                                             'diffpass/entropy_ops.py'),
                                      'diffpass.entropy_ops.smooth_mean_two_body_entropy': ( 'entropy_ops.html#smooth_mean_two_body_entropy',
                                                                                             'diffpass/entropy_ops.py')},
            'diffpass.gumbel_sinkhorn_ops': { 'diffpass.gumbel_sinkhorn_ops.gumbel_matching': ( 'gumbel_sinkhorn_ops.html#gumbel_matching',
                                                                                                'diffpass/gumbel_sinkhorn_ops.py'),
                                              'diffpass.gumbel_sinkhorn_ops.gumbel_noise_like': ( 'gumbel_sinkhorn_ops.html#gumbel_noise_like',
                                                                                                  'diffpass/gumbel_sinkhorn_ops.py'),
                                              'diffpass.gumbel_sinkhorn_ops.gumbel_sinkhorn': ( 'gumbel_sinkhorn_ops.html#gumbel_sinkhorn',
                                                                                                'diffpass/gumbel_sinkhorn_ops.py'),
                                              'diffpass.gumbel_sinkhorn_ops.inverse_permutation': ( 'gumbel_sinkhorn_ops.html#inverse_permutation',
                                                                                                    'diffpass/gumbel_sinkhorn_ops.py'),
                                              'diffpass.gumbel_sinkhorn_ops.log_sinkhorn_norm': ( 'gumbel_sinkhorn_ops.html#log_sinkhorn_norm',
                                                                                                  'diffpass/gumbel_sinkhorn_ops.py'),
                                              'diffpass.gumbel_sinkhorn_ops.matching': ( 'gumbel_sinkhorn_ops.html#matching',
                                                                                         'diffpass/gumbel_sinkhorn_ops.py'),
                                              'diffpass.gumbel_sinkhorn_ops.np_matching': ( 'gumbel_sinkhorn_ops.html#np_matching',
                                                                                            'diffpass/gumbel_sinkhorn_ops.py'),
                                              'diffpass.gumbel_sinkhorn_ops.randperm_mat_like': ( 'gumbel_sinkhorn_ops.html#randperm_mat_like',
                                                                                                  'diffpass/gumbel_sinkhorn_ops.py'),
                                              'diffpass.gumbel_sinkhorn_ops.sinkhorn_norm': ( 'gumbel_sinkhorn_ops.html#sinkhorn_norm',
                                                                                              'diffpass/gumbel_sinkhorn_ops.py'),
                                              'diffpass.gumbel_sinkhorn_ops.unbias_by_randperms': ( 'gumbel_sinkhorn_ops.html#unbias_by_randperms',
                                                                                                    'diffpass/gumbel_sinkhorn_ops.py')},
            'diffpass.model': { 'diffpass.model.Blosum62Similarities': ('model.html#blosum62similarities', 'diffpass/model.py'),
                                'diffpass.model.Blosum62Similarities.__init__': ( 'model.html#blosum62similarities.__init__',
                                                                                  'diffpass/model.py'),
                                'diffpass.model.Blosum62Similarities.forward': ( 'model.html#blosum62similarities.forward',
                                                                                 'diffpass/model.py'),
                                'diffpass.model.EnsembleMatrixApply': ('model.html#ensemblematrixapply', 'diffpass/model.py'),
                                'diffpass.model.EnsembleMatrixApply.__init__': ( 'model.html#ensemblematrixapply.__init__',
                                                                                 'diffpass/model.py'),
                                'diffpass.model.EnsembleMatrixApply.forward': ( 'model.html#ensemblematrixapply.forward',
                                                                                'diffpass/model.py'),
                                'diffpass.model.GeneralizedPermutation': ('model.html#generalizedpermutation', 'diffpass/model.py'),
                                'diffpass.model.GeneralizedPermutation.__init__': ( 'model.html#generalizedpermutation.__init__',
                                                                                    'diffpass/model.py'),
                                'diffpass.model.GeneralizedPermutation._hard_mats': ( 'model.html#generalizedpermutation._hard_mats',
                                                                                      'diffpass/model.py'),
                                'diffpass.model.GeneralizedPermutation._impl_fixed_matchings': ( 'model.html#generalizedpermutation._impl_fixed_matchings',
                                                                                                 'diffpass/model.py'),
                                'diffpass.model.GeneralizedPermutation._not_fixed_masks': ( 'model.html#generalizedpermutation._not_fixed_masks',
                                                                                            'diffpass/model.py'),
                                'diffpass.model.GeneralizedPermutation._soft_mats': ( 'model.html#generalizedpermutation._soft_mats',
                                                                                      'diffpass/model.py'),
                                'diffpass.model.GeneralizedPermutation._validate_fixed_matchings': ( 'model.html#generalizedpermutation._validate_fixed_matchings',
                                                                                                     'diffpass/model.py'),
                                'diffpass.model.GeneralizedPermutation.forward': ( 'model.html#generalizedpermutation.forward',
                                                                                   'diffpass/model.py'),
                                'diffpass.model.GeneralizedPermutation.hard_': ( 'model.html#generalizedpermutation.hard_',
                                                                                 'diffpass/model.py'),
                                'diffpass.model.GeneralizedPermutation.mode': ( 'model.html#generalizedpermutation.mode',
                                                                                'diffpass/model.py'),
                                'diffpass.model.GeneralizedPermutation.soft_': ( 'model.html#generalizedpermutation.soft_',
                                                                                 'diffpass/model.py'),
                                'diffpass.model.HammingSimilarities': ('model.html#hammingsimilarities', 'diffpass/model.py'),
                                'diffpass.model.HammingSimilarities.__init__': ( 'model.html#hammingsimilarities.__init__',
                                                                                 'diffpass/model.py'),
                                'diffpass.model.HammingSimilarities.forward': ( 'model.html#hammingsimilarities.forward',
                                                                                'diffpass/model.py'),
                                'diffpass.model.InterGroupLoss': ('model.html#intergrouploss', 'diffpass/model.py'),
                                'diffpass.model.InterGroupLoss.__init__': ('model.html#intergrouploss.__init__', 'diffpass/model.py'),
                                'diffpass.model.InterGroupLoss.forward': ('model.html#intergrouploss.forward', 'diffpass/model.py'),
                                'diffpass.model.IntraGroupLoss': ('model.html#intragrouploss', 'diffpass/model.py'),
                                'diffpass.model.IntraGroupLoss.__init__': ('model.html#intragrouploss.__init__', 'diffpass/model.py'),
                                'diffpass.model.IntraGroupLoss.forward': ('model.html#intragrouploss.forward', 'diffpass/model.py'),
                                'diffpass.model.MILoss': ('model.html#miloss', 'diffpass/model.py'),
                                'diffpass.model.MILoss.__init__': ('model.html#miloss.__init__', 'diffpass/model.py'),
                                'diffpass.model.MILoss.forward': ('model.html#miloss.forward', 'diffpass/model.py'),
                                'diffpass.model.ReciprocalBestHits': ('model.html#reciprocalbesthits', 'diffpass/model.py'),
                                'diffpass.model.ReciprocalBestHits.__init__': ( 'model.html#reciprocalbesthits.__init__',
                                                                                'diffpass/model.py'),
                                'diffpass.model.ReciprocalBestHits._hard_rbh_fn': ( 'model.html#reciprocalbesthits._hard_rbh_fn',
                                                                                    'diffpass/model.py'),
                                'diffpass.model.ReciprocalBestHits._soft_rbh_fn': ( 'model.html#reciprocalbesthits._soft_rbh_fn',
                                                                                    'diffpass/model.py'),
                                'diffpass.model.ReciprocalBestHits.forward': ('model.html#reciprocalbesthits.forward', 'diffpass/model.py'),
                                'diffpass.model.ReciprocalBestHits.hard_': ('model.html#reciprocalbesthits.hard_', 'diffpass/model.py'),
                                'diffpass.model.ReciprocalBestHits.mode': ('model.html#reciprocalbesthits.mode', 'diffpass/model.py'),
                                'diffpass.model.ReciprocalBestHits.prepare_fixed': ( 'model.html#reciprocalbesthits.prepare_fixed',
                                                                                     'diffpass/model.py'),
                                'diffpass.model.ReciprocalBestHits.soft_': ('model.html#reciprocalbesthits.soft_', 'diffpass/model.py'),
                                'diffpass.model.TwoBodyEntropyLoss': ('model.html#twobodyentropyloss', 'diffpass/model.py'),
                                'diffpass.model.TwoBodyEntropyLoss.__init__': ( 'model.html#twobodyentropyloss.__init__',
                                                                                'diffpass/model.py'),
                                'diffpass.model.TwoBodyEntropyLoss.forward': ('model.html#twobodyentropyloss.forward', 'diffpass/model.py'),
                                'diffpass.model._consecutive_slices_from_sizes': ( 'model.html#_consecutive_slices_from_sizes',
                                                                                   'diffpass/model.py')},
            'diffpass.msa_parsing': { 'diffpass.msa_parsing.read_msa': ('msa_parsing.html#read_msa', 'diffpass/msa_parsing.py'),
                                      'diffpass.msa_parsing.read_sequence': ('msa_parsing.html#read_sequence', 'diffpass/msa_parsing.py'),
                                      'diffpass.msa_parsing.remove_insertions': ( 'msa_parsing.html#remove_insertions',
                                                                                  'diffpass/msa_parsing.py')},
            'diffpass.sequence_similarity_ops': { 'diffpass.sequence_similarity_ops._reciprocate_best_hits': ( 'sequence_similarity_ops.html#_reciprocate_best_hits',
                                                                                                               'diffpass/sequence_similarity_ops.py'),
                                                  'diffpass.sequence_similarity_ops.hard_reciprocal_best_hits': ( 'sequence_similarity_ops.html#hard_reciprocal_best_hits',
                                                                                                                  'diffpass/sequence_similarity_ops.py'),
                                                  'diffpass.sequence_similarity_ops.smooth_hamming_similarities_cdist': ( 'sequence_similarity_ops.html#smooth_hamming_similarities_cdist',
                                                                                                                          'diffpass/sequence_similarity_ops.py'),
                                                  'diffpass.sequence_similarity_ops.smooth_hamming_similarities_dot': ( 'sequence_similarity_ops.html#smooth_hamming_similarities_dot',
                                                                                                                        'diffpass/sequence_similarity_ops.py'),
                                                  'diffpass.sequence_similarity_ops.smooth_substitution_matrix_similarities': ( 'sequence_similarity_ops.html#smooth_substitution_matrix_similarities',
                                                                                                                                'diffpass/sequence_similarity_ops.py'),
                                                  'diffpass.sequence_similarity_ops.soft_reciprocal_best_hits': ( 'sequence_similarity_ops.html#soft_reciprocal_best_hits',
                                                                                                                  'diffpass/sequence_similarity_ops.py')},
            'diffpass.train': { 'diffpass.train.DiffPASSResults': ('train.html#diffpassresults', 'diffpass/train.py'),
                                'diffpass.train.InformationAndReciprocalBestHits': ( 'train.html#informationandreciprocalbesthits',
                                                                                     'diffpass/train.py'),
                                'diffpass.train.InformationAndReciprocalBestHits.__init__': ( 'train.html#informationandreciprocalbesthits.__init__',
                                                                                              'diffpass/train.py'),
                                'diffpass.train.InformationAndReciprocalBestHits._adjust_cfg_and_ensemble_shape': ( 'train.html#informationandreciprocalbesthits._adjust_cfg_and_ensemble_shape',
                                                                                                                    'diffpass/train.py'),
                                'diffpass.train.InformationAndReciprocalBestHits._adjust_loss_weights_and_ensemble_shape': ( 'train.html#informationandreciprocalbesthits._adjust_loss_weights_and_ensemble_shape',
                                                                                                                             'diffpass/train.py'),
                                'diffpass.train.InformationAndReciprocalBestHits._fit': ( 'train.html#informationandreciprocalbesthits._fit',
                                                                                          'diffpass/train.py'),
                                'diffpass.train.InformationAndReciprocalBestHits._precompute_rbh': ( 'train.html#informationandreciprocalbesthits._precompute_rbh',
                                                                                                     'diffpass/train.py'),
                                'diffpass.train.InformationAndReciprocalBestHits._prepare_fit': ( 'train.html#informationandreciprocalbesthits._prepare_fit',
                                                                                                  'diffpass/train.py'),
                                'diffpass.train.InformationAndReciprocalBestHits.effective_loss_weights_': ( 'train.html#informationandreciprocalbesthits.effective_loss_weights_',
                                                                                                             'diffpass/train.py'),
                                'diffpass.train.InformationAndReciprocalBestHits.fit': ( 'train.html#informationandreciprocalbesthits.fit',
                                                                                         'diffpass/train.py'),
                                'diffpass.train.InformationAndReciprocalBestHits.forward': ( 'train.html#informationandreciprocalbesthits.forward',
                                                                                             'diffpass/train.py'),
                                'diffpass.train.InformationAndReciprocalBestHits.hard_': ( 'train.html#informationandreciprocalbesthits.hard_',
                                                                                           'diffpass/train.py'),
                                'diffpass.train.InformationAndReciprocalBestHits.soft_': ( 'train.html#informationandreciprocalbesthits.soft_',
                                                                                           'diffpass/train.py'),
                                'diffpass.train._dcc': ('train.html#_dcc', 'diffpass/train.py'),
                                'diffpass.train.apply_hard_permutation_batch_to_similarity': ( 'train.html#apply_hard_permutation_batch_to_similarity',
                                                                                               'diffpass/train.py'),
                                'diffpass.train.global_argmax_from_group_argmaxes': ( 'train.html#global_argmax_from_group_argmaxes',
                                                                                      'diffpass/train.py')}}}
