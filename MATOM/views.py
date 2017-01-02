import glob
import os

from crispy_forms.utils import render_crispy_form
from django.core.context_processors import csrf
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView, View
from jsonview.decorators import json_view
from pylab import *

import MARSTools.Assess_by_score
import MATOM.models
from MARSTools import Assess_by_score, Assess_by_score_pbm, motif_ic, run_gimme
from MARSTools.run_centrimo import run_centrimo
from MARSTools.run_fisim import run_fisim
from MARSTools.run_tomtom import run_tomtom
from MARSTools.utils import rotate_image
from MATOM import utils
from MATOM.models import ChipSeq, Matrix, Pbm, run_get_meme, run_get_meme_id
from MATOM.utils import meme_head, mkdir_p, get_path, meme_path, BASE_DIR, create_parameter_file, \
    combine_meme, handle_uploaded_bed, get_table, is_meme_uploaded, is_meme_pasted, get_parameter_dict
from models import TranscriptionFactor, ChipData, PbmData
from search.forms import AssessByComparisonForm, AssessByScoreForm, AssessByEnrichmentForm, UnknownForm, SearchForm
from search.search_code import *


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class HomePageView(TemplateView):
    template_name = 'MATOM/index.html'


class AboutView(TemplateView):
    template_name = 'MATOM/about.html'


class DocumentationView(TemplateView):
    template_name = 'MATOM/documentation.html'

class DownloadsView(TemplateView):
    template_name = 'MATOM/downloads.html'

class SearchView(AjaxableResponseMixin, FormView):
    form_class = SearchForm

    success_url = "/search"
    template_name = "search/search.html"
    # context = {'message': error_message}

    @method_decorator(json_view)
    def post(self, request, *args, **kwargs):
        # print "checking here"
        form = self.form_class(request.POST)
        if form.is_valid():

            print "then here"
            # print request.FILES['uploaded_motif']
            query_string = request.POST.get('search')
            #selected_project_id = query_string

            tf_details_dict = {
            }

            entry_query = get_query(query_string, ['tf_name', 'alt_tf_name', ])
            found_entries = TranscriptionFactor.objects.filter(entry_query)

            if len(found_entries) == 1:
                tf_class_id = found_entries[0].tf_id
                Tf_exists = Matrix.objects.filter(tf_id=tf_class_id).exists()

                chip_seq_exist = ChipSeq.objects.filter(tf_id=tf_class_id).exists()

                pbm_exitst = Pbm.objects.filter(tf_id=tf_class_id).exists()

                # TODO: Most of these should be in the models since they query DB. Keep business logic out

                import re
                if chip_seq_exist:
                    chipid = ChipSeq.objects.filter(tf_id=tf_class_id)[0].chip_id
                    chip_data = ChipData.objects.filter(chip_id=chipid).all()
                    chip_summary = []
                    for tf in chip_data:
                        a = str(tf.raw)
                        raw_file = re.split(r'([A-Z][a-z]*)', str(a))
                        cell_line = ''.join([raw_file[9], raw_file[10]])
                        lab = raw_file[7]

                        chip_summary.append([a, cell_line, lab])
                else:
                    chip_summary = []

                if pbm_exitst:
                    pbmid = Pbm.objects.filter(tf_id=tf_class_id)[0].pbm_id
                    pbm_data = PbmData.objects.filter(pbm_id=pbmid).all()
                    pbm_summary = []
                    for tf in pbm_data:
                        a = str(tf.source)

                        pbm_summary.append([a])
                else:
                    pbm_summary = []

                # Write  a function, that uses these data to get the summary information.
                #results_folder = '%s/MATOM/static/files/temp' % BASE_DIR
                #results_folder = '%s/www/MARS/static/files/%s' % (home, method)
                results_folder = "%stemp" % get_path()[0]
                mkdir_p(results_folder)

                if Tf_exists:

                    meme_out = '%s/temp.meme' % results_folder

                    with open(meme_out, "w") as out_file:
                        print "Lets get mmeme"
                        out_file.write(meme_head)

                    run_get_meme_id(tf_class_id, meme_out)

                    raw_out_file = '%s/temp_ic.txt' % results_folder

                    motif_ic.get_motif_summary_tfid(meme_out, raw_out_file, meme_path, results_folder)

                    t_head = get_table(raw_out_file)[0]
                    t_body = get_table(raw_out_file)[1]
                else:
                    t_head = []
                    t_body = []

                data = {'t_body': t_body, 't_head': t_head, 'chip_summary': chip_summary, 'pbm_summary': pbm_summary}

                return render(request, template_name='MATOM/search_summary.html', context=data)

            elif len(found_entries) == 0:
                return redirect('/search/')
            else:
                for items in found_entries:
                    if found_entries is not None:
                        tf_details_dict[items.tf_id] = items.tf_name



            #data = serializers.serialize('json', found_entries)

            request.session['selected_project_id'] = tf_details_dict

            # tf = request.POST.get('tf').lower()
            # score_method = request.POST.get("score")
            # mode = request.POST.get('mode')
            # formats = request.POST.get('formats')
            # pasted_motif = request.POST.get('test_motif')
            # uploaded_motif = self.request.FILES.get('uploaded_motif')
            # uploaded_chip = self.request.FILES.get('uploaded_chipseq')
            # data = {
            #     'found_entries': found_entries
            # }

            #form_html = render_to_string('search/search_results.html', context=data, request=request)

            #return {'success': True, 'form_html': form_html}

            return redirect('/search/select/')

        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        print "We got the form up and running"
        return {'success': False, 'form_html': form_html}


class SearchResultsView(FormView):
    form_class = UnknownForm

    success_url = "/search/select/"
    template_name = "search/search_results.html"
    # context = {'message': error_message}

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        selected_project_id = request.session.get('selected_project_id')

        tf_choices = tuple(selected_project_id.items())

        form.fields['tf_choices'].choices = tf_choices

        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(json_view)
    def post(self, request, *args, **kwargs):
        # print "checking here"
        form = self.form_class(request.POST)
        print form.is_valid()

        # TODO: Assuming for now that the form is valid

        #if form.is_valid():
        # print request.FILES['uploaded_motif']

        tf_class_id = request.POST.get('tf_choices')

        #Now lets validate available options

        Tf_exists = Matrix.objects.filter(tf_id=tf_class_id).exists()

        chip_seq_exist = ChipSeq.objects.filter(tf_id=tf_class_id).exists()

        pbm_exitst = Pbm.objects.filter(tf_id=tf_class_id).exists()

        # TODO: Most of these should be in the models since they query DB. Keep business logic out

        import re
        if chip_seq_exist:
            chipid = ChipSeq.objects.filter(tf_id=tf_class_id)[0].chip_id
            chip_data = ChipData.objects.filter(chip_id=chipid).all()
            chip_summary = []
            for tf in chip_data:
                a = str(tf.raw)
                raw_file = re.split(r'([A-Z][a-z]*)', str(a))
                cell_line = ''.join([raw_file[9], raw_file[10]])
                lab = raw_file[7]

                chip_summary.append([a, cell_line, lab])
        else:
            chip_summary = []

        if pbm_exitst:
            pbmid = Pbm.objects.filter(tf_id=tf_class_id)[0].pbm_id
            pbm_data = PbmData.objects.filter(pbm_id=pbmid).all()
            pbm_summary = []
            for tf in pbm_data:
                a = str(tf.source)

                pbm_summary.append([a])
        else:
            pbm_summary = []

        # Write  a function, that uses these data to get the summary information.
        results_folder = "%s/temp" % get_path()[0]
        print results_folder


        if Tf_exists:

            meme_out = '%stemp.meme' % results_folder

            with open(meme_out, "w") as out_file:
                print "Lets get mmeme"
                out_file.write(meme_head)

            run_get_meme_id(tf_class_id, meme_out)

            raw_out_file = '%s/temp_ic.txt' % results_folder

            motif_ic.get_motif_summary_tfid(meme_out, raw_out_file, meme_path, results_folder)

            t_head = get_table(raw_out_file)[0]
            t_body = get_table(raw_out_file)[1]
        else:
            t_head = []
            t_body = []

        data = {'t_body': t_body, 't_head': t_head, 'chip_summary': chip_summary, 'pbm_summary': pbm_summary}

        return render(request, template_name='MATOM/search_summary.html', context=data)


class AssessByScoreView(AjaxableResponseMixin, FormView):
    form_class = AssessByScoreForm

    success_url = "/assess"
    template_name = "MATOM/assess_by_score.html"

    # context = {'message': error_message}
    error_message = {
        "NO_TFID": "Sorry, Motif lacks TF_ID; working on correcting it",
        "FEW_MOTIFS": "Require more than three motifs for comparison",
        "MEME_ERROR": "There were no convincing matches to any MEME Suite motif format.",
        'REQUIRED': "",
        "NO_TF": "TF not in database, please upload or paste motifs",
        "NO_CHIP": "Motif in database but ChIP-seq is data missing, please upload",
        "BED_ERROR": "Uploaded file not in USCC BED format",
        'NO_PBM': "No PBM data for the TF in database, please upload",  # TODO: implement this option
        "NOT_AVAILABLE": "Not currently implemented, coming soon!"
    }

    @method_decorator(json_view)
    def post(self, request, *args, **kwargs):
        static_files = get_path("score")[0]
        job_no = static_files.split("/")[-1]

        meme_error = "ERROR"
        # print "checking here"
        form = self.form_class(request.POST, request.FILES)
        if request.is_ajax():
            print "then here"
            # print request.FILES['uploaded_motif']
            tf = request.POST.get('tf').lower()
            score_method = request.POST.get("score")
            mode = request.POST.get('mode')
            formats = request.POST.get('formats')
            pasted_motif = request.POST.get('test_motif')
            uploaded_motif = self.request.FILES.get('uploaded_motif')
            uploaded_chip = self.request.FILES.get('uploaded_chipseq')
            data = request.POST.get('data')
            if formats:
                if formats == 'upload' and uploaded_motif is None:
                    formats = False
                    print "Uploaded"
                if formats == 'paste' and pasted_motif == "":
                    formats = False
                    print "pasted"
            tf_exists = Matrix.objects.filter(motif_name=tf).exists()
            # pasted_motif is not u"" or uploaded_motif
            #print job_no
            if tf != "":
                #static_files = get_path("score")[0]

                #print static_files

                if tf_exists or formats:
                    results_folder = static_files
                    print "TF exists or formats"
                    motif_present_and_correct = self.handle_motifs(tf, pasted_motif, formats, results_folder, tf_exists)
                    print motif_present_and_correct

                    if not motif_present_and_correct:
                        print "Motif is all good"
                        if tf_exists:
                            print "and there is a TF"
                            tf_class_id = MATOM.models.get_tf(tf)[0]
                            chipseq_exists = ChipSeq.objects.filter(tf_id=tf_class_id).exists()

                            if data == "ChIP-seq":
                                print "So we got here"
                                chip_okay = self.process_chip(chipseq_exists, tf, results_folder)
                                if not chipseq_exists and not chip_okay:
                                    meme_error = "NO_CHIP"
                                else:
                                    if chip_okay:
                                        chip_seq_list = chip_okay

                                        results_folder_path = '%s/%s' % (static_files, tf)

                                        print results_folder_path
                                        user_motif = "%s/%s/%s.meme" % (static_files, tf, tf)
                                        files_path = '%s/%s/%s' % (results_folder, tf, tf)

                                        if mode == "ASSESS":
                                            Assess_by_score.run_all(tf, score_method, user_motif,
                                                                    chip_seq_list, results_folder_path)

                                            score_ext = Assess_by_score.score_extensions[score_method]

                                            utils.extract_scored_meme(files_path + ".meme",
                                                                      files_path + "_assess_ranked_by_" + score_ext + "_auc.meme",
                                                                      utils.get_dict_assess(files_path + "." + score_ext, "AUC"))

                                            # data = self.plot_info(mode, tf, score_method, results_folder)
                                            # form_html = render_to_string('MATOM/assess_by_score_results.html',
                                            #                              context=data, request=request)
                                            par_name = "%s/parameter_file" % results_folder
                                            create_parameter_file(par_name, tf, mode, score_method)
                                            # 'form_html': form_html
                                            return {'success': True, 'success_url': '/score/job%s' % job_no}
                                        else:
                                            run_gimme.run_gimme(tf, user_motif, chip_seq_list, results_folder_path, figure=True)

                                            utils.extract_scored_meme(files_path + ".meme", files_path + "_gimme_ranked_by_" +
                                                                      mode.lower() + "_auc.meme",
                                                                      utils.get_dict_assess(files_path + "." +
                                                                                            mode.lower(), "AUC"))
                                            par_name = "%s/parameter_file" % results_folder
                                            create_parameter_file(par_name, tf, mode, score_method)
                                            return {'success': True, 'success_url': '/score/job%s' % job_no}
                                            #meme_error = "NOT_AVAILABLE"
                                    else:
                                        meme_error = "BED_ERROR"
                            else:

                                pbm_exists = Pbm.objects.filter(tf_id=tf_class_id).exists()
                                if pbm_exists:
                                    print "We got to PBM"
                                    pbm_list = glob.glob('%s/Data/PBM/%s/*' % (BASE_DIR, tf.capitalize()))
                                    pbm_list_clean = []
                                    for pbms in pbm_list:
                                        if Assess_by_score_pbm.get_pbm_possitives(pbms) > 10:
                                            pbm_list_clean.append(pbms)
                                    if len(pbm_list_clean) > 0:
                                        print "And pbm all good"
                                        user_motif = "%s/%s/%s.meme" % (static_files, tf, tf)
                                        results_folder_path = '%s/%s' % (static_files, tf)

                                        Assess_by_score_pbm.run_all_pbm(tf, score_method, user_motif,
                                                                        pbm_list_clean, results_folder_path)

                                        files_path = '%s/%s/%s' % (results_folder, tf, tf)

                                        score_ext = Assess_by_score.score_extensions[score_method]
                                        utils.extract_scored_meme(files_path + ".meme",
                                                                      files_path + "_assess_ranked_by_" + score_ext + "_auc.meme",
                                                                      utils.get_dict_assess(files_path + "." + score_ext, "AUC"))

                                        # data = self.plot_info(mode, tf, score_method, results_folder)
                                        # form_html = render_to_string('MATOM/assess_by_score_results.html',
                                        #                              context=data, request=request)
                                        par_name = "%s/parameter_file" % results_folder
                                        create_parameter_file(par_name, tf, mode, score_method)
                                        # 'form_html': form_html,

                                        return {'success': True, 'success_url': '/score/job%s' % job_no}
                                    else:
                                        meme_error = 'NO_PBM'
                                else:
                                    meme_error = 'NO_PBM'
                        else:
                            meme_error = "NO_CHIP"
                    else:
                        meme_error = motif_present_and_correct
                else:
                    meme_error = "NO_TF"
            else:
                meme_error = "REQUIRED"
        #os.removedirs(self.static_files)
        if os.path.exists(static_files):
            import shutil
            print "We had to delete"
            shutil.rmtree(static_files)
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return {'success': False, 'form_html': form_html, 'error_message': self.error_message, 'meme_error': meme_error}

    def handle_motifs(self, tf, user_motif, formats, results_folder, tf_exists=True):
        #os.makedirs('%s/%s' % (results_folder, tf))
        mkdir_p('%s/%s' % (results_folder, tf))
        meme_out = "%s/%s/%s.meme" % (results_folder, tf, tf)
        uploaded_motif = self.request.FILES.get('uploaded_motif')

        meme_error = "MEME_ERROR"
        with open(meme_out, "w") as out_file:
            print "Lets get mmeme"
            out_file.write(meme_head)
        motif_is_correct = False
        if tf_exists:
            print "TF-exist in handle"
            tf_class_id = MATOM.models.get_tf(tf)[0]
            if tf_class_id is not None:
                motif_is_correct = True
                run_get_meme(tf, meme_out)
            else:
                meme_error = "NO_TFID"
        if formats:
            print "passed formats"
            if formats == "paste":
                motif_is_correct = is_meme_pasted(user_motif, results_folder)[0]
                if motif_is_correct:
                    combine_meme("%s/pasted.meme" % results_folder, meme_out)
            else:
                motif_is_correct = is_meme_uploaded(uploaded_motif, results_folder)[0]
                if motif_is_correct:
                    combine_meme('%s/%s' % (results_folder, uploaded_motif.name), meme_out)
        else:
            meme_error = ""
        if motif_is_correct:
            print "And motif was okay"
            if open(meme_out).read().count("MOTIF") < 3:
                meme_error = "FEW_MOTIFS"
            else:
                meme_error = False

        return meme_error


    @staticmethod
    # FIXME This function needs a lot of fixing...looking clunky
    # The function should be removed outside the class, especially the plotting should be directly linked with the
    # with the program that runs the assessment of the data.
    def plot_info(mode, tf, score_method, results_folder):
        job_no = results_folder.split("/")[-1]
        if mode == "ASSESS":
            files_path = '%s/%s/%s' % (results_folder, tf, tf)
            score_ext = Assess_by_score.score_extensions[score_method]

            display_img = '/static/files/score/%s/%s/%s_assess' % (job_no, tf, tf)
            file_in = "%s/%s/%s.%s" % (results_folder, tf, tf, score_ext)
            utils.extract_scored_meme(files_path + ".meme", files_path + "_assess_ranked_by_" + score_ext + "_auc.meme",
                                      utils.get_dict_assess(files_path + "." + score_ext, "AUC"))
            t_head = get_table(file_in)[0]
            gomer_list = get_table(file_in)[1]
            context = {'tf': tf, 'mode': mode, 'display_img': display_img, 'gomer_list': gomer_list,
                       't_head': t_head, 'score_method': Assess_by_score.score_extensions[score_method]}
        else:
            files_path = '%s/%s/%s' % (results_folder, tf, tf)
            MARSTools.run_gimme.plot_histogram_gimme(files_path + "_gimme_metrics.txt",
                                                     files_path + ".gimme", files_path + '_gimme.png')
            MARSTools.run_gimme.plot_histogram_gimme(files_path + "_gimme_metrics.txt",
                                                     files_path + ".gimme", files_path + '_gimme.eps')
            rotate_image(files_path + '_gimme.png', files_path + '_gimme_rot.png')
            display_img = '/static/files/score/%s/%s/%s_gimme' % (job_no, tf, tf)
            file_in = "%s/%s/%s.gimme" % (results_folder, tf, tf)
            t_head = get_table(file_in)[0]
            gomer_list = get_table(file_in)[1]
            utils.extract_scored_meme(files_path + ".meme", files_path + "_gimme_ranked_by_" + mode.lower() + "_auc.meme",
                                      utils.get_dict_assess(files_path + "." + mode.lower(), "AUC"))
            context = {'tf': tf, 'mode': mode, 'display_img': display_img, 'gomer_list': gomer_list,
                       't_head': t_head, 'score_method': Assess_by_score.score_extensions[score_method]}
        return context

    def process_chip(self, chipseq_exists, tf, results_folder):

        uploaded_chip = self.request.FILES.get('uploaded_chipseq')
        if chipseq_exists:
            chip_seq_list = glob.glob('%s/Data/ChIP-seq/Derived/Posneg/%s/*' % (BASE_DIR, tf.capitalize()))
            if uploaded_chip:
                bed_status = handle_uploaded_bed(tf, '100', uploaded_chip, results_folder)
                if bed_status[0]:
                    uploaded_chip = "%s/%s/%s_tmp_chip_100.posneg" % (self.static_files, tf, tf)
                    chip_seq_list.append(uploaded_chip)
                else:
                    chip_seq_list = False

        elif uploaded_chip and not chipseq_exists:
                bed_status = handle_uploaded_bed(tf, '100', uploaded_chip, results_folder)
                if bed_status[0]:
                    uploaded_chip = "%s/%s/%s_tmp_chip_100.posneg" % (self.static_files, tf, tf)
                    chip_seq_list = [uploaded_chip]
                else:
                    chip_seq_list = False
        else:
            chip_seq_list = False

        return chip_seq_list


class AssessByComparisonView(AssessByScoreView):
    static_files = get_path(method="compare")[0]
    job_no = static_files.split("/")[-1]
    form_class = AssessByComparisonForm
    success_url = "/comparison/%s" % job_no
    template_name = "MATOM/assess_by_comparison.html"


    @method_decorator(json_view)
    def post(self, request, *args, **kwargs):
        """

        """
        #static_files = self.static_files
        if request.method == 'POST':
            meme_error = None
            print "pased here"
            form = self.form_class(request.POST, request.FILES)
            if request.is_ajax():
                print "This is ajax"
                mode = request.POST.get('mode')
                tf = request.POST.get('tf')
                formats = request.POST.get('formats')
                pasted_motif = request.POST.get('test_motif')

                uploaded_motif = self.request.FILES.get('uploaded_motif')
                tf_exists = Matrix.objects.filter(motif_name=tf).exists()
                print formats
                if formats:
                    if formats == 'upload' and uploaded_motif is None:
                        formats = False
                        print "Uploaded"
                    if formats == 'paste' and pasted_motif == "":
                        formats = False
                        print "pasted"
                # Ensure some form of motif has been entered by the user
                # pasted_motif is not u"" or uploaded_motif
                if tf != "":
                    if tf_exists or formats:
                        static_files = get_path(method="compare")[0]
                        results_folder = static_files
                        motif_present_and_correct = self.handle_motifs(tf, pasted_motif, formats, results_folder, tf_exists)

                        if not motif_present_and_correct:
                            if mode == "FISIM":
                                meme_file = "%s/%s/%s.meme" % (results_folder, tf, tf)
                                file_path = "%s/%s" % (results_folder, tf)
                                run_fisim(tf, meme_file, file_path, figure=True)

                                meme_out_file = "%s/%s/%s_ranked_by_fisim.meme" % (results_folder, tf, tf)
                                raw_file = "%s/%s/%s.fisim" % (results_folder, tf, tf)
                                # TODO: These are not being properly ranked, check it out
                                utils.extract_scored_meme(meme_file, meme_out_file, utils.get_dict(raw_file))
                                raw_out_file = "%s/%s/%s_ic.txt" % (results_folder, tf, tf)
                                motif_ic.get_motif_summary(meme_file, raw_file, tf, raw_out_file, meme_path, results_folder)
                                t_head = get_table(raw_out_file)[0]
                                t_body = get_table(raw_out_file)[1]
                            else:
                                meme_file = "%s/%s/%s.meme" % (results_folder, tf, tf)
                                file_path = "%s/%s" % (results_folder, tf)
                                run_tomtom(tf, meme_file, file_path, figure=True)
                                meme_out_file = "%s/%s/%s_ranked_by_tomtom.meme" % (results_folder, tf, tf)
                                raw_file = "%s/%s/%s.tomtom" % (results_folder, tf, tf)
                                needed_dict = utils.get_dict(raw_file)
                                utils.extract_scored_meme(meme_file, meme_out_file, needed_dict)
                                raw_out_file = "%s/%s/%s_ic.txt" % (results_folder, tf, tf)
                                motif_ic.get_motif_summary(meme_file, raw_file, tf, raw_out_file, meme_path, results_folder)
                                t_head = get_table(raw_out_file)[0]
                                t_body = get_table(raw_out_file)[1]
                            job_no = results_folder.split("/")[-1]
                            display_img = '/static/files/compare/%s/%s/%s_%s.png' % (job_no, tf, tf, mode.lower())
                            data = {'tf': tf, 'mode': mode, 'display_img': display_img, 't_body': t_body, 't_head': t_head}

                            form_html = render_to_string('MATOM/assess_by_comparison_results.html', context=data, request=request)
                            ctx = {}
                            ctx.update(csrf(request))
                            par_name = "%s/parameter_file" % results_folder
                            create_parameter_file(par_name, tf, mode)
                            return {'success': True, 'form_html': form_html, 'success_url': '/comparison/job%s' % job_no}
                        else:
                            meme_error = motif_present_and_correct
                    else:
                        meme_error = "NO_TF"
                else:
                    meme_error = 'REQUIRED'
            if os.path.exists(self.static_files):
                import shutil
                shutil.rmtree(self.static_files)
            ctx = {}
            ctx.update(csrf(request))
            form_html = render_crispy_form(form, context=ctx)
            return {'success': False, 'form_html': form_html, 'error_message': self.error_message,
                    'meme_error': meme_error}


class AssessByEnrichmentView(AssessByScoreView):
    static_files = get_path(method="enrich")[0]
    form_class = AssessByEnrichmentForm
    success_url = "/enrichment"
    template_name = "MATOM/assess_by_enrichment.html"

    @method_decorator(json_view)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        meme_error = None
        if request.is_ajax():
            print "We got here "
            mode = request.POST.get('mode')
            tf = request.POST.get('tf').lower()
            pasted_motif = request.POST.get('test_motif')
            uploaded_motif = self.request.FILES.get('uploaded_motif')
            formats = request.POST.get('formats')
            if formats:
                if formats == 'upload' and uploaded_motif is None:
                    formats = False
                    print "Uploaded"
                if formats == 'paste' and pasted_motif == "":
                    formats = False
                    print "pasted"
            uploaded_chip = self.request.FILES.get('uploaded_chipseq')
            tf_exists = Matrix.objects.filter(motif_name=tf).exists()

            if tf != "":
                if tf_exists or formats:
                    static_files = get_path(method="enrich")[0]
                    results_folder = static_files
                    motif_present_and_correct = self.handle_motifs(tf, pasted_motif, formats, results_folder, tf_exists)
                    if not motif_present_and_correct:
                        if tf_exists:
                            tf_class_id = MATOM.models.get_tf(tf)[0]
                            chipseq_exists = ChipSeq.objects.filter(tf_id=tf_class_id).exists()
                            chip_okay = self.process_chip(chipseq_exists, tf, results_folder)
                            if chip_okay:
                                chip_seq_list = chip_okay
                                results_folder_path = '%s/%s' % (results_folder, tf)
                                user_motif = "%s/%s/%s.meme" % (results_folder, tf, tf)

                                if mode == "CENTRIMO":

                                    run_centrimo(tf, chip_seq_list, user_motif, results_folder_path, figure=True)

                                    meme_file = "%s/%s/%s.meme" % (results_folder, tf, tf)
                                    meme_out_file = "%s/%s/%s_ranked_by_%s.meme" % (results_folder, tf, tf, mode.lower())
                                    centrimo_raw = "%s/%s/%s_centrimo_norm.txt" % (results_folder, tf, tf)
                                    utils.extract_scored_meme(meme_file, meme_out_file, utils.get_dict(centrimo_raw))
                                    centrimo_raw = "%s/%s/%s_centrimo.txt" % (results_folder, tf, tf)
                                    t_head = get_table(centrimo_raw)[0]
                                    t_body = get_table(centrimo_raw)[1]
                                    job_no = results_folder.split("/")[-1]
                                    display_img = '/static/files/enrich/%s/%s/%s_centrimo' % (job_no, tf, tf)

                                    data = {'display_img': display_img, 'tf': tf, 'mode': mode,
                                        't_body': t_body, 't_head': t_head}

                                    form_html = render_to_string('MATOM/assess_by_enrichment_results.html',
                                                             context=data, request=request)
                                    ctx = {}
                                    ctx.update(csrf(request))

                                    par_name = "%s/parameter_file" % results_folder
                                    create_parameter_file(par_name, tf, mode)

                                    return {'success': True, 'form_html': form_html, 'success_url': '/enrichment/job%s' % job_no}
                                else:
                                    meme_error = 'NOT_AVAILABLE'
                                    #context = {'message': error_message, 'form': form, 'tf': tf}
                                    #return render(request, 'MATOM/assess_by_enrichment.html', context)

                            else:
                                meme_error = "BED_ERROR"
                        else:
                            meme_error = 'NO_CHIP'
                    else:
                        meme_error = motif_present_and_correct
                else:
                    meme_error = "NO_TF"
            else:
                meme_error = "REQUIRED"

        if os.path.exists(self.static_files):
            import shutil
            shutil.rmtree(self.static_files)

        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return {'success': False, 'form_html': form_html, 'error_message': self.error_message, 'meme_error': meme_error}


###############################################################################
#       Results display view
###############################################################################

class GetResultsCompare(View):

    def get(self, request, slug, *args, **kwargs):

        job_no = request.path_info.split("job")[-1]

        results_folder = "%s/compare/%s" % (get_path()[0], str(job_no))
        par_name = "%s/parameter_file" % results_folder

        if os.path.isfile(par_name):

            parameters = get_parameter_dict(par_name)

            tf = parameters['tf']
            mode = parameters['mode']

            raw_out_file = "%s/%s/%s_ic.txt" % (results_folder, tf, tf)
            t_head = get_table(raw_out_file)[0]
            t_body = get_table(raw_out_file)[1]

            display_img = '/static/files/compare/%s/%s' % (job_no, tf)
            data = {'tf': tf, 'mode': mode, 'display_img': display_img, 't_body': t_body, 't_head': t_head}

            return render(request, 'MATOM/assess_by_comparison_results.html', context=data)
        else:
            return render(request, '404.html')


class GetResultsScore(View):

    def get(self, request, slug, *args, **kwargs):

        job_no = request.path_info.split("job")[-1]
        print job_no

        results_folder = "%s/score/%s" % (get_path()[0], str(job_no))
        par_name = "%s/parameter_file" % results_folder

        if os.path.isfile(par_name):

            parameters = get_parameter_dict(par_name)

            tf = parameters['tf']
            mode = parameters['mode']
            score_method = parameters['score']

            data = self.plot_info(mode, tf, score_method, results_folder)

            return render(request, 'MATOM/assess_by_score_results.html', context=data)
        else:
            return render(request, '404.html')

    @staticmethod
    def plot_info(mode, tf, score_method, results_folder):
        job_no = results_folder.split("/")[-1]
        if mode == "ASSESS":
            score_ext = Assess_by_score.score_extensions[score_method]

            display_img = '/static/files/score/%s/%s/%s_assess' % (job_no, tf, tf)
            file_in = "%s/%s/%s.%s" % (results_folder, tf, tf, score_ext)
            t_head = get_table(file_in)[0]
            gomer_list = get_table(file_in)[1]

            context = {'tf': tf, 'mode': mode, 'display_img': display_img, 'gomer_list': gomer_list,
                       't_head': t_head, 'score_method': Assess_by_score.score_extensions[score_method]}
        else:

            display_img = '/static/files/score/%s/%s/%s_gimme' % (job_no, tf, tf)
            file_in = "%s/%s/%s.gimme" % (results_folder, tf, tf)
            t_head = get_table(file_in)[0]
            gomer_list = get_table(file_in)[1]

            context = {'tf': tf, 'mode': mode, 'display_img': display_img, 'gomer_list': gomer_list,
                       't_head': t_head, 'score_method': Assess_by_score.score_extensions[score_method]}
        return context


class GetResultsEnrich(View):

    def get(self, request, slug, *args, **kwargs):

        job_no = request.path_info.split("job")[-1]

        results_folder = "%s/enrich/%s" % (get_path()[0], str(job_no))
        par_name = "%s/parameter_file" % results_folder

        if os.path.isfile(par_name):

            parameters = get_parameter_dict(par_name)

            tf = parameters['tf']
            mode = parameters['mode']

            centrimo_raw = "%s/%s/%s_centrimo.txt" % (results_folder, tf, tf)
            t_head = get_table(centrimo_raw)[0]
            t_body = get_table(centrimo_raw)[1]
            job_no = results_folder.split("/")[-1]
            display_img = '/static/files/enrich/%s/%s/' % (job_no, tf)

            data = {'display_img': display_img, 'tf': tf, 'mode': mode,
                                        't_body': t_body, 't_head': t_head}

            return render(request, 'MATOM/assess_by_enrichment_results.html', context=data)
        else:
            return render(request, '404.html')


class TfChoiceView(AjaxableResponseMixin, FormView):
    form_class = UnknownForm
    success_url = "/search"
    template_name = "MATOM/assess_by_enrichment.html"

    @method_decorator(json_view)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

