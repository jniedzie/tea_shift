#ifndef ShiftHistogramsFiller_hpp
#define ShiftHistogramsFiller_hpp

#include "Event.hpp"
#include "EventProcessor.hpp"
#include "Helpers.hpp"
#include "HistogramsHandler.hpp"

class ShiftHistogramsFiller {
 public:
  ShiftHistogramsFiller(std::shared_ptr<HistogramsHandler> histogramsHandler_);
  ~ShiftHistogramsFiller();

  void Fill(const std::shared_ptr<Event> event, bool initial);

 private:
  std::shared_ptr<HistogramsHandler> histogramsHandler;
  std::unique_ptr<EventProcessor> eventProcessor;
  std::string weightsBranchName;

  float GetWeight(const std::shared_ptr<Event> event);

  void FillZprimeHistograms(const std::shared_ptr<Event> event);
  void FillDarkPhotonHistograms(const std::shared_ptr<Event> event);
  void FillDarkHadronsHistograms(const std::shared_ptr<Event> event);
  void FillMuonHistograms(const std::shared_ptr<Event> event, std::string collectionName, std::string histName);
};

#endif /* ShiftHistogramsFiller_hpp */
