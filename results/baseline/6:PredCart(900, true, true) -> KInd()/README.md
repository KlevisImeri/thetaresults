Multiplier = 4 
learning is for 5 
          if(statsHolder.iteration > 4  // INFO: you have to at least learn the weights a bit 
            //  2^8 = 256 complete states is quite small if you are using whole
            && now > cegarParams.explosionMultiplier*predictedTimeMs) {
            throw StateSpaceExplosionException();
          }
