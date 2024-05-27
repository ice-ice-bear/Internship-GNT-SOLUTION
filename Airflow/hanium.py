from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup

import pendulum

with DAG(f'hanium',
         description="data_preperation_and_model_launch",
         start_date=pendulum.datetime(2022, 1, 1 ,tz="Asia/Seoul"),
         schedule_interval = None,
         catchup=False) as dag:
    
    
    s1 = BashOperator(
        task_id="LLM",
        bash_command= 'sleep 5'
    )

    with TaskGroup(group_id='Math') as tg_1:

        with TaskGroup(group_id='Math_Data_Preperation') as m_ig_1:

            m2_1 = BashOperator(
                task_id="read_math_pdf_file",
                bash_command= 'sleep 5'
            )

            m2_2 = BashOperator(
                task_id="read_grade_school_math_json_file",
                bash_command= 'sleep 5'
            )

            m3_1 = BashOperator(
                task_id="extract_text_from_pdf_file_using_keyword",
                bash_command= 'sleep 5'
            )

            m3_2 = BashOperator(
                task_id="device_each_pair_into_txt_file",
                bash_command= 'sleep 5'
            )

            m4_1 = BashOperator(
                task_id="clense_data_into_trainable_format",
                bash_command= 'sleep 5'
            )

            m4_2 = BashOperator(
                task_id="translate_english_into_korean",
                bash_command= 'sleep 5'
            )

            m5_1 = BashOperator(
                task_id="modify_txt_file_into_json_file",
                bash_command= 'sleep 5'
            )

            m5_2 = BashOperator(
                task_id="rewrite_txt_file_into_json_file",
                bash_command= 'sleep 5'
            )

            m2_1 >> m3_1 >> m4_1 >> m5_1
            m2_2 >> m3_2 >> m4_2 >> m5_2

        with TaskGroup(group_id='alpaca_llm_custom_data_training') as m_ig_2:

            m6 = BashOperator(
                task_id="run_custom_data_training",
                bash_command= 'sleep 5'
            )

            m7 = BashOperator(
                task_id="distribute_model_with_langchain_js",
                bash_command= 'sleep 5'
            )

            m6 >> m7

        with TaskGroup(group_id='back_end_math_model_deploy') as m_ig_3:

            m8 = BashOperator(
                task_id="Build_and_prepare_the_server_environment",
                bash_command= 'sleep 5'
            )

            m9 = BashOperator(
                task_id="Set_up_API_endpoints_and_routes",
                bash_command= 'sleep 5'
            )

            m10 = BashOperator(
                task_id="Authentication_and_Security",
                bash_command= 'sleep 5'
            )

            m11 = BashOperator(
                task_id="Generate_and_return_a_response",
                bash_command= 'sleep 5'
            )
            
            m12 = BashOperator(
                task_id="Error_handling_and_exception_handling",
                bash_command= 'sleep 5'
            )

            m13 = BashOperator(
                task_id="Test_and_Optimize",
                bash_command= 'sleep 5'
            )

            m14 = BashOperator(
                task_id="Deployment_and_Operations",
                bash_command= 'sleep 5'
            )

            m8 >> m9 >> m10 >> m11 >> m12 >> m13 >> m14

        m_ig_1 >> m_ig_2 >> m_ig_3


    with TaskGroup(group_id='English') as tg_2:
            
        with TaskGroup(group_id='Math_Data_Preperation') as e_ig_1:

            e2 = BashOperator(
                task_id="read_english_pdf_file",
                bash_command= 'sleep 5'
            )

            e3 = BashOperator(
                task_id="extract_text_from_pdf_file",
                bash_command= 'sleep 5'
            )

            e4 = BashOperator(
                task_id="remain_only_english_word",
                bash_command= 'sleep 5'
            )

            e5 = BashOperator(
                task_id="distinguish_words_according_to_parts_of_speech",
                bash_command= 'sleep 5'
            )
            

            e2 >> e3 >> e4 >> e5

        with TaskGroup(group_id='dall_e_image_generation') as e_ig_2:
            
            e6 = BashOperator(
                task_id="make_english_text_prompt_according_to_parts_of_speech",
                bash_command= 'sleep 5'
            )

            e7 = BashOperator(
                task_id="Generate_image_using_DALL_E_2",
                bash_command= 'sleep 5'
            )

            e8 = BashOperator(
                task_id="distribute_image_and_keyword_data_to_backend",
                bash_command= 'sleep 5'
            )

            e6 >>  e7 >> e8

        with TaskGroup(group_id='back_end_english_quiz_deploy') as e_ig_3:

            with TaskGroup(group_id='front_end') as e_ig_3_1:

                e9 = BashOperator(
                    task_id="front_select_an_image",
                    bash_command= 'sleep 5'
                )

                e10 = BashOperator(
                    task_id="upload_an_image",
                    bash_command= 'sleep 5'
                )

                e11 = BashOperator(
                    task_id="request_HTTP",
                    bash_command= 'sleep 5'
                )

                e9 >> e10 >> e11
            
            e12 = BashOperator(
                task_id="receiving_requests",
                bash_command= 'sleep 5'
            )
            
            e13 = BashOperator(
                task_id="image_processing",
                bash_command= 'sleep 5'
            )

            e14 = BashOperator(
                task_id="image_format",
                bash_command= 'sleep 5'
            )            
                            
            e15 = BashOperator(
                task_id="image_analysis",
                bash_command= 'sleep 5'
            )
            
            e16 = BashOperator(
                task_id="specify_the_output_format",
                bash_command= 'sleep 5'
            )

            e17 = BashOperator(
                task_id="process_error",
                bash_command= 'sleep 5'
            )            

            e18 = BashOperator(
                task_id="security",
                bash_command= 'sleep 5'
            )                

            e19 = BashOperator(
                task_id="performance_optimization",
                bash_command= 'sleep 5'
            )

            e20 = BashOperator(
                task_id="testing",
                bash_command= 'sleep 5'
            )

            e21 = BashOperator(
                task_id="documentation",
                bash_command= 'sleep 5'
            )

            e_ig_3_1 >> e12 >> e13 >> e14 >> e15 >> e16 >> e17 >> e18 >> e19 >> e20 >> e21        

        e_ig_1 >> e_ig_2 >> e_ig_3




s1 >> [tg_1, tg_2]







    
    