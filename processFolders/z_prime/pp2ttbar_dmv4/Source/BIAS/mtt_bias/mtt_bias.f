C ************************************************************
C Source for the library implementing a bias function that 
C populates the large pt tale of the leading jet. 
C
C The two options of this subroutine, that can be set in
C the run card are:
C    > (double precision) mtt_bias_offset : target mtt value
C
C
C Schematically, the functional form of the enhancement is
C    bias_wgt = [mtt(evt)/mean_mtt]^enhancement_power
C ************************************************************
C
C The following lines are read by MG5aMC to set what are the 
C relevant parameters for this bias module.
C
C  parameters = {'mtt_bias_offset': 2000.0}
C

      subroutine bias_wgt(p, original_weight, bias_weight)
          implicit none
C
C Parameters
C
          include '../../maxparticles.inc'          
          include '../../nexternal.inc'

C
C Arguments
C
          double precision p(0:3,nexternal)
          double precision pTot(0:3)
          double precision mtt
          double precision original_weight, bias_weight
C
C local variables
C
          integer i,j
          double precision pt(nexternal)
          double precision max_mtt
          double precision polynomial_arg
          double precision polynomial_offset
c
c local variables defined in the run_card
c
          double precision mtt_bias_offset
C
C Global variables
C
C
C Mandatory common block to be defined in bias modules
C
          double precision stored_bias_weight
          data stored_bias_weight/1.0d0/          
          logical impact_xsec, requires_full_event_info
C         We only want to bias distributions, but not impact the xsec. 
          data impact_xsec/.False./
C         Of course this module does not require the full event
C         information (color, resonances, helicities, etc..)
          data requires_full_event_info/.False./ 
          common/bias/stored_bias_weight,impact_xsec,
     &                requires_full_event_info

C
C Accessingt the details of the event
C
          logical is_a_j(nexternal),is_a_l(nexternal),
     &            is_a_b(nexternal),is_a_a(nexternal),
     &            is_a_onium(nexternal),is_a_nu(nexternal),
     &            is_heavy(nexternal),do_cuts(nexternal)
          common/to_specisa/is_a_j,is_a_a,is_a_l,is_a_b,is_a_nu,
     &                      is_heavy,is_a_onium,do_cuts
C
C    Setup the value of the parameters from the run_card    
C
      include '../bias.inc'

C --------------------
C BEGIN IMPLEMENTATION
C --------------------
          
          bias_weight = 1.0d0
          mtt = 0d0
          pTot = (/ 0d0, 0d0, 0d0, 0d0 /)
          do i=1,nexternal
            if (is_heavy(i)) then
            ! if (abs(idup(i,1,1)).eq.6) then
              do j =0,3
                pTot(j) = pTot(j)+p(j,i)
              enddo 
            endif
          enddo

          mtt = dsqrt(pTot(0)**2 - pTot(1)**2 - pTot(2)**2 - pTot(3)**2)
      
          if (mtt.gt.0.0d0) then
            ! Calculate the offset once using Region 2 coefficients
            polynomial_offset = - (8.77777447d-07 * mtt_bias_offset**2 - 6.83274463d-03 * mtt_bias_offset + 6.87312584d+00)

            if (mtt .lt. 1050.0d0) then
              ! Region 1 (Quadratic)
              polynomial_arg = - (7.69602876d-07 * mtt**2 - 7.37667598d-03 * mtt + 7.56808623d+00)

            else if (mtt .ge. 1050.0d0 .and. mtt .lt. 1850.0d0) then
              ! Region 2 (Quadratic)
              polynomial_arg = - (8.77777447d-07 * mtt**2 - 6.83274463d-03 * mtt + 6.87312584d+00)

            else if (mtt .ge. 1850.0d0 .and. mtt .lt. 2100.0d0) then
              ! Region 3 (Cubic)
              polynomial_arg = - (-2.15204002d-07 * mtt**3 + 1.25075909d-03 * mtt**2 - 2.42291486d+00 * mtt + 1.56151760d+03)

            else if (mtt .ge. 2100.0d0 .and. mtt .lt. 3100.0d0) then
              ! Region 4 (Quadratic)
              polynomial_arg = - (3.75563446d-07 * mtt**2 - 5.17596861d-03 * mtt + 5.59054274d+00)

            else if (mtt .ge. 3100.0d0 .and. mtt .lt. 4500.0d0) then
              ! Region 5 (Quadratic)
              polynomial_arg = - (1.51047189d-07 * mtt**2 - 3.89233044d-03 * mtt + 3.79105692d+00)

            else
              ! Region 6 (Quadratic)
              mtt = min(mtt, 6000.0d0)
              polynomial_arg = - (-7.38435410d-08 * mtt**2 - 1.84673563d-03 * mtt - 9.67738736d-01)
            endif

            bias_weight = EXP(polynomial_arg - polynomial_offset)
          endif

      return

      end subroutine bias_wgt
