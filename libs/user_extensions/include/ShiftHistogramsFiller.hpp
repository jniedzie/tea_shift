#ifndef ShiftHistogramsFiller_hpp
#define ShiftHistogramsFiller_hpp

#include "Event.hpp"
#include "EventProcessor.hpp"
#include "Helpers.hpp"
#include "HepMCParticle.hpp"
#include "HistogramsHandler.hpp"
#include "HepMCProcessor.hpp"

class ShiftHistogramsFiller {
 public:
  ShiftHistogramsFiller(std::shared_ptr<HistogramsHandler> histogramsHandler_);
  ~ShiftHistogramsFiller();

  void Fill(const std::shared_ptr<Event> event, bool initial);

 private:
  std::shared_ptr<HistogramsHandler> histogramsHandler;
  std::unique_ptr<EventProcessor> eventProcessor;
  std::unique_ptr<HepMCProcessor> hepMCProcessor;
  std::string weightsBranchName;

  float GetWeight(const std::shared_ptr<Event> event);

  void FillZprimeHistograms(const std::shared_ptr<Event> event);
  void FillDarkPhotonHistograms(const std::shared_ptr<Event> event);
  void FillDarkHadronsHistograms(const std::shared_ptr<Event> event);
  void FillMuonHistograms(const std::shared_ptr<Event> event, std::string collectionName, std::string histName, double minEnergy = 0.0,
                          bool usePt = false);

  void FillSingleMuonHistograms(std::shared_ptr<HepMCParticle> hepMCParticle, std::string histName, double eventWeight);
  void FillDimuonHistograms(std::shared_ptr<HepMCParticle> hepMCParticle, std::shared_ptr<HepMCParticle> hepMCParticle2,
                            std::string histName, double eventWeight);

  void Fill2Dhistograms(const std::shared_ptr<Event> event);
};

#endif /* ShiftHistogramsFiller_hpp */
